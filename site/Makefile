.PHONY: check test verify deploy-dry-run deploy

BUCKET ?= s3://tetrasemaphore.systems-site
REGION ?= us-west-2
DIST_ID ?= E1EMF780M9UOHH

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

deploy: check
	aws s3 sync . $(BUCKET) --region $(REGION) $(ALLOWLIST)
	for f in index.html note.html method.html 404.html; do \
		aws s3 cp "$$f" "$(BUCKET)/$$f" --region $(REGION) --content-type "text/html; charset=utf-8" --cache-control "no-cache"; \
	done
	for f in robots.txt llms.txt .well-known/security.txt; do \
		aws s3 cp "$$f" "$(BUCKET)/$$f" --region $(REGION) --content-type "text/plain; charset=utf-8" --cache-control "no-cache"; \
	done
	aws s3 cp sitemap.xml "$(BUCKET)/sitemap.xml" --region $(REGION) --content-type "application/xml; charset=utf-8" --cache-control "no-cache"
	aws cloudfront create-invalidation --distribution-id $(DIST_ID) --paths "/*"
