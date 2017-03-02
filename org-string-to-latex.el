#!emacs --script

;; This is not needed anymore, since it turns out that org-mode has its own
;; "org-export-string-as" function that essentially does the same.

(require 'org)

(setq mstr (pop command-line-args-left))

(with-temp-buffer
  (insert mstr)
  (org-latex-export-as-latex nil nil nil t)  ; the true is to assure that the output is the body only
  (with-current-buffer  "*Org LATEX Export*"
    (princ (buffer-string))))

;; with-output-to-string could have been a useful macro
