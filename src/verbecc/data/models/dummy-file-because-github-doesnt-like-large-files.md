I have removed the `trained_model-<lang>.zip` files as GitHub does not
appreciate such large files (approx. 252M total for 6 languages) nor does `pypi`, 
it as rejects the `verbecc` wheel file unless I remove the zips prior to building.  

This file is a workaround for an install error I experienced regarding this directory
not existing. Having any file such as this dummy file in this directory avoids this
issue and `verbecc` will then regenerate the model zips and save them into this directory.

As you may know, Git only tracks files, not directories, so this file ensures that
the `models` directory continues to exist when this repo is cloned.
