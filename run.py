import sys

import ims

host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
ims.run(host)
