extract:
	pybabel extract --input-dirs=apps -o locales/messages.pot
ru_faylini_yaratish:
	 pybabel init -i locales/messages.pot -d locales -D messages -l ru
po_faylida_ozgarish_qilinganda:
	pybabel compile -d locales -D messages
yangi_tarjima_qoshilganda:
	pybabel extract --input-dirs=apps -o locales/messages.pot -k _
	pybabel update -i locales/messages.pot -d locales -D messages
