(TeX-add-style-hook
 "relatorio"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "12pt")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("fontenc" "T1") ("babel" "brazil") ("inputenc" "utf8")))
   (add-to-list 'LaTeX-verbatim-environments-local "lstlisting")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "lstinline")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "lstinline")
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art12"
    "fontenc"
    "algorithm2e"
    "sbc-template"
    "babel"
    "inputenc"
    "listings")
   (LaTeX-add-labels
    "section:intro"
    "section:primeira"
    "section:primeira:estruturas"
    "section:primeira:algoritmos"
    "section:primeira:algoritmos:escadinha"
    "section:primeira:resultados"
    "table:resultados-1")
   (LaTeX-add-environments
    '("lyxlist" 1))))

