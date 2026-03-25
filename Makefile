build:
	pelican -s publishconf.py

deploy: build
	@read -p "EPFL username: " user; \
	lftp -u $$user ic-ftps.epfl.ch -e "mirror --reverse --delete --verbose output/ plfm.epfl.ch; bye"

clean:
	rm -rf output/

.PHONY: build deploy clean
