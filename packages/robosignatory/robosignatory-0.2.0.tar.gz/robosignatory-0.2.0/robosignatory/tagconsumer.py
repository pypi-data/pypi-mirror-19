import koji

import fedmsg
import fedmsg.consumers
import robosignatory.utils as utils

import logging
log = logging.getLogger("robosignatory.tagconsumer")


class TagSignerConsumer(fedmsg.consumers.FedmsgConsumer):
    config_key = 'robosignatory.enabled.tagsigner'

    def __init__(self, hub):
        if hub:
            super(TagSignerConsumer, self).__init__(hub)
            self.config = self.hub.config
        else:
            # No hub, we are in ad-hoc mode
            self.config = fedmsg.config.load_config()
            logging.basicConfig(level=logging.DEBUG)

        prefix = self.config.get('topic_prefix')
        env = self.config.get('environment')
        self.topic = [
            '%s.%s.buildsys.tag' % (prefix, env)
        ]

        signing_config = self.hub.config['robosignatory.signing']
        self.signer = utils.get_signing_helper(**signing_config)

        self.koji_clients = {}
        for instance in self.config['robosignatory.koji_instances']:
            instance_info = self.config[
                'robosignatory.koji_instances'][instance]
            client = koji.ClientSession(instance_info['url'],
                                        instance_info['options'])

            if instance_info['options']['authmethod'] == 'ssl':
                client.ssl_login(instance_info['options']['cert'],
                                 None,
                                 instance_info['options']['serverca'])
            elif instance_info['options']['authmethod'] == 'kerberos':
                kwargs = {}
                for opt in ('principal', 'keytab', 'ccache'):
                    if opt in instance_info['options']:
                        kwargs[opt] = instance_info['options'][opt]
                client.krb_login(**kwargs)
            else:
                raise Exception('Only SSL and kerberos authmethods supported')

            instance_obj = {'client': client,
                            'tags': {}}
            for tag in instance_info['tags']:
                if tag['from'] in instance_obj['tags']:
                    raise Exception('From detected twice: %s' % tag['from'])
                instance_obj['tags'][tag['from']] = {'to': tag['to'],
                                                     'key': tag['key'],
                                                     'keyid': tag['keyid']}

            self.koji_clients[instance] = instance_obj

            log.info('TagSignerConsumer ready for service')

    def consume(self, msg):
        topic = msg['topic']
        if topic not in self.topic:
            return

        msg = msg['body']['msg']

        #  {u'build_id': 799208,
        #   u'name': u'python-fmn-rules',
        #   u'tag_id': 374,
        #   u'instance': u'primary',
        #   u'tag': u'epel7-infra',
        #   u'user': u'puiterwijk',
        #   u'version': u'0.9.1',
        #   u'owner': u'sayanchowdhury',
        #   u'release': u'1.el7'}}

        build_nvr = '%(name)s-%(version)s-%(release)s' % msg
        build_id = msg['build_id']
        tag = msg['tag']
        koji_instance = msg['instance']

        self.dowork(build_nvr, build_id, tag, koji_instance,
                    skip_tagging=False)

    def dowork(self, build_nvr, build_id, tag, koji_instance,
               skip_tagging=False):
        log.info('Build %s (%s) tagged into %s on %s',
                 build_nvr, build_id, tag, koji_instance)

        if koji_instance not in self.koji_clients:
            log.info('Koji instance not known, skipping')
            return

        instance = self.koji_clients[koji_instance]
        if tag not in instance['tags']:
            log.info('Tag not autosigned, skipping')
            return

        if not build_id:
            build_id = instance['client'].findBuildID(build_nvr)

        tag_info = instance['tags'][tag]
        log.info('Going to sign with %s (%s) and move to %s',
                 tag_info['key'], tag_info['keyid'], tag_info['to'])

        rpms = utils.get_rpms(instance['client'],
                              build_nvr=build_nvr,
                              build_id=build_id,
                              sigkey=tag_info['keyid'])
        log.info('RPMs to sign and move: %s',
                 ['%s (%s, signed: %s)' %
                    (key, rpms[key]['id'], rpms[key]['signed'])
                    for key in rpms.keys()])
        if len(rpms) < 1:
            log.info('Build contains no rpms, skipping')
            return

        if all([rpms[rpm]['signed'] for rpm in rpms]):
            log.debug('All RPMs are already signed')
        else:
            to_sign = [key for key in rpms.keys() if not rpms[key]['signed']]
            log.debug('RPMs needing signing: %s' % to_sign)
            cmdline = self.signer.build_sign_cmdline(tag_info['key'],
                                                     rpms.keys(),
                                                     koji_instance)
            log.debug('Signing command line: %s' % cmdline)

            ret, stdout, stderr = utils.run_command(cmdline)
            if ret != 0:
                log.error('Error signing! Signing output: %s, stdout: '
                          '%s, stderr: %s', ret, stdout, stderr)
                return

        log.info('Build was succesfully signed, telling koji to write with key'
                 ' %s', tag_info['keyid'])

        for rpm in rpms:
            instance['client'].writeSignedRPM(rpms[rpm]['id'],
                                              tag_info['keyid'])

        log.info('Signed RPMs written out')

        if skip_tagging:
            log.info('Tagging skipped, done')
        else:
            log.info('Packages correctly signed, moving to %s' %
                     tag_info['to'])
            if tag == tag_info['to']:
                log.info('Non-gated, not moving')
            else:
                instance['client'].tagBuild(tag_info['to'], build_id, False,
                                            tag)
