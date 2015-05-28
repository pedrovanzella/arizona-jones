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
    "testeprof"
    "testebobo"
    "article"
    "art12"
    "fontenc"
    "algorithm2e"
    "dot2texi"
    "tikz"
    "sbc-template"
    "babel"
    "inputenc"
    "listings")
   (LaTeX-add-labels
    "sec:intro"
    "sec:estruturas"
    "fig:testeprof"
    "sec:entrada"
    "fig:testebobo"
    "sec:algoritmos"
    "sec:algoritmos:criar-nodos"
    "sec:algoritmos:criar-arestas"
    "sec:algoritmos:comparar"
    "sec:algoritmos:base6"
    "sec:algoritmos:calcular-tamanho-caminhos"
    "sec:algoritmos:vizinhos-que-chegam"
    "sec:algoritmos:achar-maior-caminho"
    "sec:algoritmos:encontrar-maior-peso"
    "sec:algoritmos:main"
    "sec:resultados"
    "tab:resultados-1")
   (LaTeX-add-environments
    '("lyxlist" 1))))

