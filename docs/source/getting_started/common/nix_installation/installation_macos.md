# macOS 11+

* **Minimum Requirements**
    * macOS 11 (Big Sur)
    * 4th Gen Intel® Core CPU or later
    * 8 GiB of RAM
    
* **Recommended**
    * macOS 11 (Big Sur)
    * Apple Silicon CPU
    * 16 GiB of RAM

## Installing Nix

Simply run this (entire) command in `Terminal.app` (the cache is shared with openlane):

```console
$ sh <(curl -L https://nixos.org/nix/install) --yes --nix-extra-conf-file /dev/stdin <<EXTRA_NIX_CONF
extra-experimental-features = nix-command flakes
extra-substituters = https://openlane.cachix.org
extra-trusted-public-keys = openlane.cachix.org-1:qqdwh+QMNGmZAuyeQJTH9ErW57OWSvdtuwfBKdS254E=
EXTRA_NIX_CONF
```

Enter your password if prompted. This should take around 5 minutes.

Make sure to close all terminals after you're done with this step.

```{include} _common.md
:heading-offset: 1

```
