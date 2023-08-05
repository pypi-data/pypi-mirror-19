# -*- coding: utf-8 -*-
from logilab.common.testlib import tag
from cubicweb import Binary

from cubes.mediaplayer.testlib import MediaPlayerBaseTestCase
from cubes.mediaplayer.utils.media import (
    id3infos, fprobe_media, reencode_sound, get_sound_formats,
    )


class MediaPlayerSoundFileTC(MediaPlayerBaseTestCase):

    @tag('length')
    def test_sound_length(self):
        with self.admin_access.repo_cnx() as cnx:
            sound = self.add_sound(cnx, self.datapath('beep.mp3'))
            cnx.commit()
            sound.cw_clear_all_caches()
            self.assertEqual(sound.length, 0)
            self.assertEqual(sound.formatted_duration, '00:00')

    @tag('id3', 'update', 'title')
    def test_id3_update_title(self):
        with self.admin_access.repo_cnx() as cnx:
            sound = self.add_sound(cnx, self.datapath('beep.mp3'))
            self.assertEqual(sound.title, 'beep.mp3')
            with open(self.datapath('bird.mp3'), 'rb') as fobj:
                sound.cw_set(data=Binary(fobj.read()))
            cnx.commit()
            sound.cw_clear_all_caches()
            self.assertEqual(sound.title, 'Singing birds')

    @tag('id3',)
    def test_id3_format(self):
        with self.admin_access.repo_cnx() as cnx:
            sound = self.add_sound(cnx, self.datapath('beep.mp3'))
            with open(self.datapath('beep.mp3'), 'rb') as fobj:
                self.assertDictEqual(dict(id3infos(sound)),
                                     dict(id3infos(fobj)))

    @tag('encode')
    def test_encode_mp3_sound(self):
        with self.admin_access.repo_cnx() as cnx:
            sound = self.add_sound(cnx, self.datapath('beep.mp3'))
            cnx.commit()
            sound.cw_clear_all_caches()
            self.assertIsNotNone(sound.data_mp3)
            self.assertEqual(sound.data_mp3_format, u'audio/mp3')
            self.assertEqual(len(sound.data_mp3.getvalue()), 13312)
            self.assertIsNotNone(sound.data_oga)
            self.assertEqual(sound.data_oga_format, u'audio/oga')
            self.assertGreater(len(sound.data_oga.getvalue()), 15000)

    @tag('encode')
    def test_encode_encoding_error(self):
        with self.admin_access.repo_cnx() as cnx:
            sound = self.add_sound(cnx, self.datapath(u'invalidé.mp3'))
            outputs = get_sound_formats(sound)
            outputs = reencode_sound(sound, outputs)
            self.assertTrue(outputs['oga'])
            self.assertFalse(sound.data_oga)
            self.assertTrue(outputs['mp3'])
            self.assertFalse(sound.data_mp3)

    @tag('encode')
    def test_probe_media(self):
        with self.admin_access.repo_cnx() as cnx:
            sound = self.add_sound(cnx, self.datapath('beep.mp3'))
            cnx.commit()
            meta = probe_media(sound)
            self.assertEqual(0.940408, meta['length'])
            self.assertEqual(109978, meta['audiodatarate'])

    def test_idownloadable(self):
        with self.admin_access.repo_cnx() as cnx:
            sound = self.add_sound(cnx, self.datapath('beep.mp3'))
            cnx.commit()
            idownloadable = sound.cw_adapt_to('IDownloadable')
            self.assertEqual(idownloadable.download_url(),
                             u'http://testing.fr/cubicweb/%s/%s/raw' % (
                sound.__regid__.lower(), sound.eid))
            self.assertEqual(idownloadable.download_content_type(),
                             'audio/mpeg')
            mpeg_adaptor = sound.cw_adapt_to('MpegIDownloadable')
            self.assertEqual(mpeg_adaptor.download_file_name(),
                             'beep.mp3')
            self.assertEqual(mpeg_adaptor.download_url(),
                             u'http://testing.fr/cubicweb/%s/%s/mp3' % (
                sound.__regid__.lower(), sound.eid))
            ogg_adaptor = sound.cw_adapt_to('OggIDownloadable')
            self.assertEqual(ogg_adaptor.download_url(),
                             u'http://testing.fr/cubicweb/%s/%s/oga' % (
                sound.__regid__.lower(), sound.eid))
            self.assertEqual(ogg_adaptor.download_file_name(),
                             'beep.oga')


if __name__ == '__main__':
    import logging
    from logilab.common.testlib import unittest_main
    logging.basicConfig(level=logging.ERROR)
    unittest_main()
