from PIL import Image
import glob, os, sys
d = sys.argv[1]
for p in sorted(glob.glob(os.path.join(d, "*.png"))):
    im = Image.open(p)
    print("%-42s %s mode=%s %3dKB" % (os.path.basename(p), im.size, im.mode, os.path.getsize(p) // 1024))
