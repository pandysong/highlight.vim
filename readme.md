![screen](screen.png)

# highlight.vim

Lost in various `#ifdef` macro definition in a large c programs like u-boot or
Linux? This plugin may help out of pain.

This vim plugin loads the match patterns from a file which is a serialized
dictionary with the file name as key and pattern as value. When a buffer is
loaded, the plugin will search the dictionary and find the pattern and set the
pattern using `matchadd` vim function, which add the pattern to a highlight
group "highlight_active_lines".

# How to use

## HighlightAdd <filename>

Use this command to add the file to the database.

The content of the files is like this:

```
{'test.vim': '\%1l\|\%3l\|\%5l', 'test2.vim': '\%1l\|\%2l\|\%3l'}
```

The pattern format like `\%1l\|\%3l\|\%5l`  means match line 1 or line 3 or line
5, where '\' is the escape character for `%` and `|`.  using `:help pattern` to
find more details. Note that the format of the database is limited by the vim
de-serialization  functions which is not quite tolerant  e.g. If there is a new
line after `,`, it fails to load the database.

Theoretically you may add any patterns to the key values and vim will
highlight it for you.

The original idea to create such a plugin is to highlight the active c code
which is used in actually in compilation to generate machine code.

### gen.py

A tool (in directory `tools`) is created to convert the file name and line
number information to the database which could be loaded using `HighlightAdd`
function.

```
python3 tools/gen.py /home/pandy/u-boot-2018.09 ../u-boot-2018.09/lines.txt \
> ../u-boot-2018.09/active_lines.txt
```

Where lines.txt looks like:

```
/home/pandy/u-boot-2018.09/arch/arm/cpu/armv8/start.S:31
/home/pandy/u-boot-2018.09/arch/arm/cpu/armv8/start.S:31
/home/pandy/u-boot-2018.09/arch/arm/cpu/armv8/start.S:31
/home/pandy/u-boot-2018.09/arch/arm/cpu/armv8/start.S:31
/home/pandy/u-boot-2018.09/arch/arm/cpu/armv8/start.S:57
/home/pandy/u-boot-2018.09/arch/arm/cpu/armv8/start.S:95
/home/pandy/u-boot-2018.09/arch/arm/cpu/armv8/start.S:104
/home/pandy/u-boot-2018.09/arch/arm/cpu/armv8/start.S:105
/home/pandy/u-boot-2018.09/arch/arm/cpu/armv8/start.S:106
/home/pandy/u-boot-2018.09/arch/arm/cpu/armv8/start.S:107
/home/pandy/u-boot-2018.09/arch/arm/cpu/armv8/start.S:108
/home/pandy/u-boot-2018.09/arch/arm/cpu/armv8/start.S:109
/home/pandy/u-boot-2018.09/arch/arm/cpu/armv8/start.S:114
/home/pandy/u-boot-2018.09/arch/arm/cpu/armv8/start.S:115
/home/pandy/u-boot-2018.09/arch/arm/cpu/armv8/start.S:116
/home/pandy/u-boot-2018.09/arch/arm/cpu/armv8/start.S:117
/home/pandy/u-boot-2018.09/arch/arm/cpu/armv8/start.S:118
/home/pandy/u-boot-2018.09/arch/arm/cpu/armv8/start.S:119
/home/pandy/u-boot-2018.09/arch/arm/cpu/armv8/start.S:120
```

Each line is with the file path name followed by `:` and then the line number.

The converted file could now be loaded with command `HighlightAdd`. Note that this
command could be called multiple times to load the different databases.

## HighlightReset

Use this command reset the dictionary database to empty.

## Customize the highlight color

Currently the highlight color is hard coded, you could customize the color using
a command similar with below command:

```
:highlight highlight_active_lines ctermbg=darkred guibg=darkred
```

## Todo

This is a very preliminary implementation. We may add function to invert the
match and low light the content which is not in the dictionary.
