# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = pymlconf
SOURCEDIR     = .
BUILDDIR      = ./_build
DEPLOYDIR     = ./../../pymlconf.io
HOME  := $(shell echo $HOME)

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile deploy livehtml

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

deploy:
	cp -rT $(BUILDDIR)/html $(DEPLOYDIR)

livehtml:
	sphinx-autobuild . -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html --watch=../$(SPHINXPROJ)
