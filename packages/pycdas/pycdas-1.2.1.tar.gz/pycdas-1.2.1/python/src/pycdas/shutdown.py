import subprocess, signal, os
p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
out, err = p.communicate()

print "Killing zombie workers: "
for line in out.splitlines():
   if 'pycdas/worker.py' in line:
     print " >> " + line
     pid = int(line.split(None, 1)[0])
     os.kill(pid, signal.SIGKILL)