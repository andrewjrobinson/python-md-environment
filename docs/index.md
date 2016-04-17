# Environment Extension

mdx_environment is a Python Markdown extension that adds tags for content based on environment variables.



## Environment values

To add values to your document that are stored in environment variables.

### Minimal

**syntax**:

```text
*Host*: \env{MY_VAR}
```

```sh
export MY_VAR="andrewjrobinson.github.io"
```

**Example**:

*Host*: \env{MY_VAR}

**html**:

```html
<p>
	<em>Host</em>: 
	<span class="environment_env" id="env0">andrewjrobinson.github.io</span>
</p>
```

### Operations

You can process the value with some basic operations

```sh
export CAMEL="tHe CaMeL sAiD"
```

```sh
\env{CAMEL}{upper}
# "THE CAMEL SAID"

\env{CAMEL}{lower}
# "the camel said"

\env{CAMEL}{title}
# "The Camel Said"

\env{CAMEL}{sentence}
# "The camel said"
```

## Conditional content

TODO: finish this documentation

### Set / unset variables

**syntax**:

```text
\if{MY_VAR}
Content that is only rendered if MY_VAR is set and has a value other than: "0", "", "false", "f", "no", "n"
\endif

\if{!MY_VAR}
Content that is only rendered if MY_VAR is NOT set or has a value: "0", "", "false", "f", "no", "n"
\endif

```

### Operators

You can check that an Environment variable matches a constant with various operators

**String comparisons**:

NOTE: No quoting and cannot include spaces at ends or '}'

I.e. 2 is not the same as 2.0

```text
\if{MY_NUM == 2}
\if{MY_STR == Hello world}

\if{MY_NUM != 2}
```

**Number comparisons**:

```text
\if{MY_NUM > 2}

\if{MY_NUM < 2}

\if{MY_NUM >= 2}

\if{MY_NUM <= 2}
```

## Typical usage

 

### \_MD\_ENV\_LOADED\_ variable

The extension will print a warning on the python logger if the \_MD\_ENV\_LOADED\_ environment variable is
not set.  This makes it easy to remember that you forgot to load your environment variables.  It
is recommended that you create a enviro/defaults.sh script that you *source* from each of your context 
scripts.

### Suggested directory structure

It is recommended that you create a *defaults.sh* file that is *sourced* by all your context specific
environment files.  If you put the \_MD\_ENV\_LOADED\_ variable in the defaults.sh file then users will
automatically get a warning message if they forget to *source* one of your context files.

*enviro/defaults.sh*:
```sh
#!/bin/bash
# default variables used by workshops

# Hide the warning about env not loaded
export _MD_ENV_LOADED_=1

export MY_VAR="andrewjrobinson.github.io"

export CAMEL="I have one hUMp"
```

*enviro/context1.sh*:
```sh
#!/bin/bash
# overrides for context 1

## import defaults ##
source enviro/defaults.sh

## Override values for this context ##
export CAMEL="I have two hUmPs"
```

*enviro/env-examples.sh*:
```sh
#!/bin/bash
# overrides for this documentation

## import defaults ##
source enviro/defaults.sh

## Override values for this context ##
export CAMEL="tHe CaMeL sAiD"
```
