# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from distutils import spawn
import os
import signal
import subprocess

import testtools


class TestCli(testtools.TestCase):

    @testtools.skipUnless(spawn.find_executable("memcached"),
                          "memcached not found")
    def test_cli(self):
        self.assertEqual(0, os.system(
            "pifpaf run memcached --port 11216 echo >/dev/null 2>&1"))

    @testtools.skipUnless(spawn.find_executable("memcached"),
                          "memcached not found")
    def test_eval(self):
        c = subprocess.Popen(["pifpaf", "run", "memcached", "--port", "11219"],
                             stdout=subprocess.PIPE)
        self.assertEqual(0, c.wait())
        env = {}
        for line in c.stdout.readlines():
            k, _, v = line.partition(b"=")
            env[k] = v
        os.kill(int(env[b"export PIFPAF_PID"].strip()[:-1]), signal.SIGTERM)

        self.assertEqual(b"\"memcached://localhost:11219\";\n",
                         env[b"export PIFPAF_URL"])
        self.assertEqual(b"\"memcached://localhost:11219\";\n",
                         env[b"export PIFPAF_MEMCACHED_URL"])

    @testtools.skipUnless(spawn.find_executable("memcached"),
                          "memcached not found")
    def test_env_prefix(self):
        c = subprocess.Popen(["pifpaf",
                              "--env-prefix", "FOOBAR",
                              "run", "memcached", "--port", "11215"],
                             bufsize=0,
                             stdout=subprocess.PIPE)
        (stdout, stderr) = c.communicate()
        self.assertEqual(0, c.wait())
        env = {}
        for line in stdout.split(b"\n"):
            k, _, v = line.partition(b"=")
            env[k] = v
        os.kill(int(env[b"export PIFPAF_PID"].strip()[:-1]), signal.SIGTERM)

        self.assertEqual(b"\"memcached://localhost:11215\";",
                         env[b"export FOOBAR_URL"])
        self.assertEqual(b"\"memcached://localhost:11215\";",
                         env[b"export FOOBAR_MEMCACHED_URL"])

    @testtools.skipUnless(spawn.find_executable("memcached"),
                          "memcached not found")
    def test_global_urls_varibale(self):
        c = subprocess.Popen(["pifpaf",
                              "--env-prefix", "FOOBAR",
                              "run", "memcached", "--port", "11217",
                              "--",
                              "pifpaf",
                              "run", "memcached", "--port", "11218"],
                             bufsize=0,
                             stdout=subprocess.PIPE)
        (stdout, stderr) = c.communicate()
        self.assertEqual(0, c.wait())
        env = {}
        for line in stdout.split(b"\n"):
            k, _, v = line.partition(b"=")
            env[k] = v
        os.kill(int(env[b"export PIFPAF_PID"].strip()[:-1]), signal.SIGTERM)

        self.assertEqual(b"\"memcached://localhost:11218\";",
                         env[b"export PIFPAF_URL"])
        self.assertEqual(b"\"memcached://localhost:11218\";",
                         env[b"export PIFPAF_MEMCACHED_URL"])
        self.assertEqual(
            b"\"memcached://localhost:11217;memcached://localhost:11218\";",
            env[b"export PIFPAF_URLS"])
