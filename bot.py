Skip to content
businessnakagawaryota-ship-it
ai-bot
Repository navigation
Code
Issues
Pull requests
Actions
Projects
Wiki
Security and quality
1
 (1)
Insights
Settings
run-video-bot
run-video-bot #46
All jobs
Run details
run
failed now in 17s
Search logs
1s
1s
0s
9s
Downloading urllib3-2.7.0-py3-none-any.whl (131 kB)
Downloading websockets-16.0-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (184 kB)
Downloading python_dotenv-1.2.2-py3-none-any.whl (22 kB)
Downloading gTTS-2.5.4-py3-none-any.whl (29 kB)
Downloading click-8.1.8-py3-none-any.whl (98 kB)
Downloading moviepy-2.2.1-py3-none-any.whl (129 kB)
Downloading pillow-11.3.0-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (6.6 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.6/6.6 MB 179.8 MB/s  0:00:00
Downloading decorator-5.3.1-py3-none-any.whl (10 kB)
Downloading imageio-2.37.3-py3-none-any.whl (317 kB)
Downloading proglog-0.1.12-py3-none-any.whl (6.3 kB)
Downloading annotated_types-0.7.0-py3-none-any.whl (13 kB)
Downloading certifi-2026.4.22-py3-none-any.whl (135 kB)
Downloading cryptography-48.0.0-cp311-abi3-manylinux_2_34_x86_64.whl (4.7 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.7/4.7 MB 309.6 MB/s  0:00:00
Downloading cffi-2.0.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (215 kB)
Downloading h11-0.16.0-py3-none-any.whl (37 kB)
Downloading imageio_ffmpeg-0.6.0-py3-none-manylinux2014_x86_64.whl (29.5 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 29.5/29.5 MB 270.6 MB/s  0:00:00
Downloading numpy-2.4.6-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (16.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 16.9/16.9 MB 331.3 MB/s  0:00:00
Downloading pyasn1_modules-0.4.2-py3-none-any.whl (181 kB)
Downloading pyasn1-0.6.3-py3-none-any.whl (83 kB)
Downloading typing_inspection-0.4.2-py3-none-any.whl (14 kB)
Downloading pycparser-3.0-py3-none-any.whl (48 kB)
Downloading sniffio-1.3.1-py3-none-any.whl (10 kB)
Downloading tqdm-4.67.3-py3-none-any.whl (78 kB)
Installing collected packages: websockets, urllib3, typing-extensions, tqdm, tenacity, sniffio, python-dotenv, pycparser, pyasn1, pillow, numpy, imageio_ffmpeg, idna, h11, distro, decorator, click, charset_normalizer, certifi, annotated-types, typing-inspection, requests, pydantic-core, pyasn1-modules, proglog, imageio, httpcore, cffi, anyio, pydantic, moviepy, httpx, gtts, cryptography, google-auth, google-genai
Successfully installed annotated-types-0.7.0 anyio-4.13.0 certifi-2026.4.22 cffi-2.0.0 charset_normalizer-3.4.7 click-8.1.8 cryptography-48.0.0 decorator-5.3.1 distro-1.9.0 google-auth-2.53.0 google-genai-2.4.0 gtts-2.5.4 h11-0.16.0 httpcore-1.0.9 httpx-0.28.1 idna-3.15 imageio-2.37.3 imageio_ffmpeg-0.6.0 moviepy-2.2.1 numpy-2.4.6 pillow-11.3.0 proglog-0.1.12 pyasn1-0.6.3 pyasn1-modules-0.4.2 pycparser-3.0 pydantic-2.13.4 pydantic-core-2.46.4 python-dotenv-1.2.2 requests-2.34.2 sniffio-1.3.1 tenacity-9.1.4 tqdm-4.67.3 typing-extensions-4.15.0 typing-inspection-0.4.2 urllib3-2.7.0 websockets-16.0
3s
Run python bot.py
Traceback (most recent call last):
=== BOT START ===
  File "/home/runner/work/ai-bot/ai-bot/bot.py", line 24, in <module>
    main()
  File "/home/runner/work/ai-bot/ai-bot/bot.py", line 13, in main
    video_path = make_video("assets/mio.jpg", voice_path)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/ai-bot/ai-bot/video_editor.py", line 16, in make_video
    subprocess.run(cmd, check=True)
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/subprocess.py", line 548, in run
    with Popen(*popenargs, **kwargs) as process:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/subprocess.py", line 1026, in __init__
    self._execute_child(args, executable, preexec_fn, close_fds,
  File "/opt/hostedtoolcache/Python/3.11.15/x64/lib/python3.11/subprocess.py", line 1955, in _execute_child
    raise child_exception_type(errno_num, err_msg, err_filename)
FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'
Error: Process completed with exit code 1.
0s
0s
1s
Post job cleanup.
/usr/bin/git version
git version 2.54.0
Temporarily overriding HOME='/home/runner/work/_temp/8a21cedd-5399-4994-8582-3a7cf8450fcf' before making global git config changes
Adding repository directory to the temporary git global config as a safe directory
/usr/bin/git config --global --add safe.directory /home/runner/work/ai-bot/ai-bot
/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
http.https://github.com/.extraheader
/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :"
/usr/bin/git config --local --name-only --get-regexp ^includeIf\.gitdir:
/usr/bin/git submodule foreach --recursive git config --local --show-origin --name-only --get-regexp remote.origin.url
0s
