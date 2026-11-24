.PHONY: check test verify deploy-dry-run deploy

BUCKET ?= s3://tetrasemaphore.systems-site
REGION ?= us-west-2
DIST_ID ?= E1EMF780M9UOHH

# The films are not copied into site/: the ten files named below, in semaphores/films/ at the repository root, are
# the ones served, uploaded one by one to assets/films/ in the bucket with their content types. The names are fixed
# here, not globbed, and the folder and the two lists are set with override, so a value given on the command line
# or in the environment does not replace them. verify.sh seals the ten hashes in that folder, admits nothing else
# there (apart from a Finder .DS_Store), requires these two lists to equal its own, WebM and MP4 each, and seals
# this file.
override FILMS_DIR := ../semaphores/films
override FILMS_WEBM := \
	CRITICAL-semaphore-three-moves.webm \
	METACOGNITIVE-semaphore-three-moves.webm \
	NON-NORMATIVE-semaphore-three-moves.webm \
	NORMATIVE-semaphore-three-moves.webm \
	TETRASEMAPHORE-four-own-moves-loop.webm
override FILMS_MP4 := \
	CRITICAL-semaphore-three-moves.mp4 \
	METACOGNITIVE-semaphore-three-moves.mp4 \
	NON-NORMATIVE-semaphore-three-moves.mp4 \
	NORMATIVE-semaphore-three-moves.mp4 \
	TETRASEMAPHORE-four-own-moves-loop.mp4

ALLOWLIST := \
	--exclude "*" \
	--include "index.html" \
	--include "note.html" \
	--include "method.html" \
	--include "404.html" \
	--include "robots.txt" \
	--include "llms.txt" \
	--include "sitemap.xml" \
	--include ".well-known/security.txt" \
	--include "assets/og-card.jpg" \
	--include "assets/og-card.png" \
	--include "assets/TETRASEMAPHORE-NORMATIVE-en-512.png" \
	--include "assets/TETRASEMAPHORE-NON-NORMATIVE-en-512.png" \
	--include "assets/TETRASEMAPHORE-METACOGNITIVE-en-512.png" \
	--include "assets/TETRASEMAPHORE-CRITICAL-en-512.png" \
	--include "assets/TETRASEMAPHORE-NORMATIVE-es-512.png" \
	--include "assets/TETRASEMAPHORE-NON-NORMATIVE-es-512.png" \
	--include "assets/TETRASEMAPHORE-METACOGNITIVE-es-512.png" \
	--include "assets/TETRASEMAPHORE-CRITICAL-es-512.png" \
	--include "assets/TETRASEMAPHORE-NORMATIVE-en-1298.png" \
	--include "assets/TETRASEMAPHORE-NON-NORMATIVE-en-1298.png" \
	--include "assets/TETRASEMAPHORE-METACOGNITIVE-en-1298.png" \
	--include "assets/TETRASEMAPHORE-CRITICAL-en-1298.png" \
	--include "assets/TETRASEMAPHORE-NORMATIVE-es-1298.png" \
	--include "assets/TETRASEMAPHORE-NON-NORMATIVE-es-1298.png" \
	--include "assets/TETRASEMAPHORE-METACOGNITIVE-es-1298.png" \
	--include "assets/TETRASEMAPHORE-CRITICAL-es-1298.png"

check:
	@./verify.sh

test: check

verify: check

deploy-dry-run: check
	aws s3 sync . $(BUCKET) --region $(REGION) $(ALLOWLIST) --dryrun
	for f in $(FILMS_WEBM); do \
		aws s3 cp "$(FILMS_DIR)/$$f" "$(BUCKET)/assets/films/$$f" --region $(REGION) --content-type "video/webm" --dryrun || exit 1; \
	done
	for f in $(FILMS_MP4); do \
		aws s3 cp "$(FILMS_DIR)/$$f" "$(BUCKET)/assets/films/$$f" --region $(REGION) --content-type "video/mp4" --dryrun || exit 1; \
	done

deploy: check
	aws s3 sync . $(BUCKET) --region $(REGION) $(ALLOWLIST)
	for f in index.html note.html method.html 404.html; do \
		aws s3 cp "$$f" "$(BUCKET)/$$f" --region $(REGION) --content-type "text/html; charset=utf-8" --cache-control "no-cache" || exit 1; \
	done
	for f in robots.txt llms.txt .well-known/security.txt; do \
		aws s3 cp "$$f" "$(BUCKET)/$$f" --region $(REGION) --content-type "text/plain; charset=utf-8" --cache-control "no-cache" || exit 1; \
	done
	aws s3 cp sitemap.xml "$(BUCKET)/sitemap.xml" --region $(REGION) --content-type "application/xml; charset=utf-8" --cache-control "no-cache"
	for f in $(FILMS_WEBM); do \
		aws s3 cp "$(FILMS_DIR)/$$f" "$(BUCKET)/assets/films/$$f" --region $(REGION) --content-type "video/webm" || exit 1; \
	done
	for f in $(FILMS_MP4); do \
		aws s3 cp "$(FILMS_DIR)/$$f" "$(BUCKET)/assets/films/$$f" --region $(REGION) --content-type "video/mp4" || exit 1; \
	done
	aws cloudfront create-invalidation --distribution-id $(DIST_ID) --paths "/*"

# This Makefile is never remade: GNU make would otherwise read it, rebuild it from a sibling such as Makefile.sh
# through a built-in suffix rule, and start again on the rebuilt file. The explicit empty rule for the file and the
# empty suffix list stop that; -r drops the remaining built-in rules.
MAKEFLAGS += -r
.SUFFIXES:
Makefile: ;
