````{admonition} If you already have Nix set up…
:class: note 

You will need to enable CACE's
[Binary Cache](https://nixos.wiki/wiki/Binary_Cache) manually.

If you don't know what that means:

We use a service called Cachix, which allows the reproducible Nix builds to be
stored on a cloud server so you do not have to build CACE's dependencies
from scratch on every computer, which will take a long time.

First, you want to install Cachix by running the following in your terminal:

```console
$ nix-env -f "<nixpkgs>" -iA cachix
```

Then set up the binary cache as follows (the cache is shared with openlane):

```console
$ sudo env PATH="$PATH" cachix use openlane
```

…and restart the Nix daemon.

```console
$ sudo pkill nix-daemon
```

---

If you *do* know what this means, the values are as follows:

```ini
extra-substituters = https://openlane.cachix.org
extra-trusted-public-keys = openlane.cachix.org-1:qqdwh+QMNGmZAuyeQJTH9ErW57OWSvdtuwfBKdS254E=
```

Make sure to restart `nix-daemon` after updating `/etc/nix/nix.conf`.

```console
$ sudo pkill nix-daemon
```

````

# Cloning CACE

With git installed, just run the following:

```console
$ git clone https://github.com/efabless/cace
```

That's it. Whenever you want to use CACE, run `nix-shell` in the repository root
directory and you'll have a full CACE environment. The first time might take
around 10 minutes while binaries are pulled from the cache.

To quickly test your installation, simply run `cace --help` in the nix
shell.
