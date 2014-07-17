@set GEVENT_LOOP=uvent.loop.UVLoop
@set GEVENT_RESOLVER=block
@set GOAGENT_LISTEN_VISIBLE=1
@start "GoAgent" "%~dp0python27.exe" "%~dp0proxy.py"
