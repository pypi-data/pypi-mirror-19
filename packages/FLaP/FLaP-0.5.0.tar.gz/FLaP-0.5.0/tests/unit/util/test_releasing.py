#
# This file is part of Flap.
#
# Flap is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Flap is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Flap.  If not, see <http://www.gnu.org/licenses/>.
#

from distutils.dist import Distribution
from unittest import TestCase, main

from flap.util.releasing import Version, Release, SourceControl
from unittest.mock import MagicMock, call, patch, ANY, mock_open


class VersionTest(TestCase):

    @staticmethod
    def makeVersion(text):
        return Version.from_text(text)

    def verifyVersion(self, version, major, minor, micro):
        self.assertTrue(version.has_major(major))
        self.assertTrue(version.has_minor(minor))
        self.assertTrue(version.has_micro(micro))

    def testPrepareDevelopmentRelease(self):
        v1 = self.makeVersion("1.0.1")
        v2 = v1.next_micro_release()
        self.verifyVersion(v2, 1, 0, 2)

    def testPrepareMinorRelease(self):
        v1 = self.makeVersion("1.0")
        v2 = v1.next_minor_release()
        self.verifyVersion(v2, 1, 1, 0)
        
    def testPrepareMajorRelease(self):
        v1 = self.makeVersion("1.0")
        v2 = v1.next_major_release()
        self.verifyVersion(v2, 2, 0, 0)
                
    def testEquality(self):
        v1 = self.makeVersion("1.3.dev1")
        self.assertTrue(v1 == v1)

    def testDifference(self):
        v1 = self.makeVersion("1.3.dev2")
        v2 = self.makeVersion("1.3.dev3")
        self.assertTrue(v1 != v2)

    def test_read_from_source_code(self):
        with patch("flap.__version__", "1.3.4"):
            version = Version.from_source_code()
            self.assertEqual(version, Version(1, 3, 4))

    def test_update_source_code(self):
        mock = mock_open(read_data="__version__ = \"1.2.3\"")
        with patch('flap.util.releasing.open', mock, create=True):
            Version.update_source_code(Version(1, 3, 0))
        mock().write.assert_called_once_with("__version__ = \"1.3.0\"")


class SourceControlTest(TestCase):

    @staticmethod
    def test_commit():
        mock = MagicMock()
        with patch("subprocess.call", mock):
            scm = SourceControl()
            scm.commit("my message")
        mock.assert_has_calls([call(["git.exe", "add", "-u"], env=ANY, shell=True),
                               call(["git.exe", "commit", "-m", "my message"], env=ANY, shell=True)])

    @staticmethod
    def test_tag():
        mock = MagicMock()
        with patch("subprocess.call", mock):
            scm = SourceControl()
            scm.tag(Version(2, 0, 1))
        mock.assert_has_calls([call(["git.exe", "tag", "-a", "v2.0.1", "-m", "\"Version 2.0.1\""], env=ANY, shell=True)])


class ReleaseTest(TestCase):

    @staticmethod
    def createSourceWithVersion(text):
        return None

    @staticmethod
    def release(scm, kind):
        release = Release(Distribution(), scm)
        release.run_command = MagicMock()
        release.type = kind
        release.run()
        return release

    @staticmethod
    def createSCM():
        scm = SourceControl()
        scm.tag = MagicMock()
        scm.commit = MagicMock()
        return scm

    @staticmethod
    def _verify_command_invocations(release):
        release.run_command.assert_has_calls([
            call("bdist_egg"),
            call("sdist"),
            call("register"),
            call("upload"),
        ])

    @patch("flap.util.releasing.Version.from_source_code", return_value=Version(1, 3, 3))
    @patch("flap.util.releasing.Version.update_source_code")
    def testMicroRelease(self, write_version, read_version):
        scm = self.createSCM()

        release = self.release(scm, "micro")

        self._verify_command_invocations(release)

        scm.tag.assert_called_once_with(Version(1, 3, 3))
        read_version.assert_called_once_with()
        write_version.assert_called_once_with(Version(1, 3, 4))
        scm.commit.assert_called_once_with("Preparing version 1.3.4")

    @patch("flap.util.releasing.Version.from_source_code", return_value=Version(1, 3, 3))
    @patch("flap.util.releasing.Version.update_source_code")
    def testMinorRelease(self, write_version, read_version):
        scm = self.createSCM()
        
        release = self.release(scm, "minor")

        self._verify_command_invocations(release)

        read_version.assert_called_once_with()
        scm.tag.assert_called_once_with(Version(1, 4, 0))
        write_version.assert_has_calls([call(Version(1, 4, 0)),
                                        call(Version(1, 4, 1))])
        scm.commit.assert_has_calls([call("Releasing version 1.4.0"),
                                     call("Preparing version 1.4.1")])

    @patch("flap.util.releasing.Version.from_source_code", return_value=Version(1, 3, 3))
    @patch("flap.util.releasing.Version.update_source_code")
    def testMajorRelease(self, write_version, read_version):
        scm = self.createSCM()
        
        release = self.release(scm, "major")

        self._verify_command_invocations(release)

        read_version.assert_called_once_with()
        scm.tag.assert_called_once_with(Version(2, 0, 0))
        write_version.assert_has_calls([call(Version(2, 0, 0)), call(Version(2, 0, 1))])
        scm.commit.assert_has_calls([call("Releasing version 2.0.0"),
                                     call("Preparing version 2.0.1")])
     
     
if __name__ == "__main__":
    main()