import sys
import thulac

seg_only = False

if(argv[3] == "-seg_only"):
	seg_only = True
lac = thulac.thulac(seg_only=seg_only)
lac.cut_f(argv[1], argv[2])