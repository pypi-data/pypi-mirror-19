import psutil


def proces_monitor():
    """Collect system process information"""
    ad_pids = []
    procs = []
    for proc in psutil.process_iter():
        try:
            mem = proc.memory_full_info()
            info = proc.as_dict(attrs=["cmdline", "username"])
        except psutil.AccessDenied:
            ad_pids.append(proc.pid)
        except psutil.NoSuchProcess:
            pass
        else:
            proc._uss = mem.uss
            proc._rss = mem.rss
            if not proc._uss:
                continue
            proc._pss = getattr(mem, "pss", "")
            proc._swap = getattr(mem, "swap", "")
            proc._info = info
            procs.append(proc)

    procs.sort(key=lambda proc: proc._uss)
    templ = "%-7s %-7s %-30s %7s %7s %7s %7s"
    print(templ % ("PID", "User", "Cmdline", "USS", "PSS", "Swap", "RSS"))
    print("=" * 78)
    for p in procs[:86]:
        line = templ % (
            p.pid,
            p._info["username"][:7],
            " ".join(p._info["cmdline"])[:30],
            bytes(p._uss),
            bytes(p._pss) if p._pss != "" else "",
            bytes(p._swap) if p._swap != "" else "",
            bytes(p._rss),
        )
        print(line)
    if ad_pids:
        print("warning: access denied for %s pids" % (len(ad_pids)))
