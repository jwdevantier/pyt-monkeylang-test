import subprocess as s

def post_process(fpath: str) -> str:
    print(f"post_process({fpath})")
    cmd = ['gofmt', '-w', fpath]
    try:
        s.check_output(cmd, stderr=s.STDOUT)
    except s.CalledProcessError as e:
        print(f"{' '.join(cmd)} => {e.returncode}")
        print('   ', end='')
        print(e.stdout.decode('UTF-8').replace('\n', '\n   '))
        raise e
    return fpath