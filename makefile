# Need to export as ENV var
export TEMPLATE_DIR = templates

PTML_DIR = html_src
ADIR = ansible
SDIR = assembler
ODIR = Emu86/templates
MUDIR = myutils
UDIR = utils
TDIR = tests
SRCS = $(SDIR)/arithmetic.py $(SDIR)/control_flow.py $(SDIR)/data_mov.py $(SDIR)/interrupts.py 
INTER2 = $(ODIR)/help.ptml
OBJS = $(ODIR)/help.html
EXTR = $(UDIR)/extract_doc.awk
D2HTML = $(UDIR)/doc2html.awk
INCS = $(TEMPLATE_DIR)/head.txt $(TEMPLATE_DIR)/navbar.txt

HTMLFILES = $(shell ls $(PTML_DIR)/*.ptml | sed -e 's/.ptml/.html/' | sed -e 's/html_src\///')

%.html: $(PTML_DIR)/%.ptml $(INCS)
	python3 $(UDIR)/html_checker.py $<
	$(UDIR)/html_include.awk <$< >$@
	git add $@

local: $(HTMLFILES)

website: $(INCS) $(HTMLFILES)
	-git commit -a 
	git pull origin master
	git push origin master

help.html: $(SRCS)
	$(EXTR) <$(SDIR)/parse.py | $(D2HTML) >$(TEMPLATE_DIR)/data.txt
	$(EXTR) <$(SDIR)/arithmetic.py | $(D2HTML) >$(TEMPLATE_DIR)/arithmetic.txt
	$(EXTR) <$(SDIR)/control_flow.py | $(D2HTML) >$(TEMPLATE_DIR)/control_flow.txt
	$(EXTR) <$(SDIR)/data_mov.py | $(D2HTML) >$(TEMPLATE_DIR)/data_mov.txt
	$(EXTR) <$(SDIR)/interrupts.py | $(D2HTML) >$(TEMPLATE_DIR)/interrupts.txt
	$(UDIR)/html_include.awk <$(ODIR)/help.ptml >$(ODIR)/help.html
	-git commit $(ODIR)/help.html

dev: $(SRCS) $(OBJS) 
	$(TDIR)/test_assemble.py
	$(TDIR)/test_errors.py
	$(TDIR)/test_control_flow.py
	$(TDIR)/test_programs.py
	-git commit -a
	git push origin master
	ssh emu86@ssh.pythonanywhere.com 'cd /home/emu86/Emu86; /home/emu86/Emu86/myutils/dev.sh'

prod: $(SRCS) $(OBJ)
	$(TDIR)/test_assemble.py
	$(TDIR)/test_errors.py
	$(TDIR)/test_control_flow.py
	$(TDIR)/test_programs.py
	git push origin master
	ssh gcallah@ssh.pythonanywhere.com 'cd /home/gcallah/Emu86; /home/gcallah/Emu86/myutils/prod.sh'

# for future use:
#	ansible-playbook -i $(ADIR)/inventories/hosts $(ADIR)/dev.yml
