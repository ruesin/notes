---
title: 让你在终端飞起来 - Mac版
date: 2016-01-26 10:08:32
categories: 本地
---

首先，要知道mac默认使用的shell是主流的bash，对于shell的理解版本等，网上资料一大堆，不做赘述。

当然，如果你坚持使用mac自带默认终端，无可非议。至少我刚使用的时候用了好久，但是mac默认终端也是让人很不爽的，不能补全命令让人很是蛋疼，解决办法：

`$ nano .inputrc`添加一下三行

```
set completion-ignore-case on
set show-all-if-ambiguous on
TAB： menu-complete
```

好了，下面开始进入正题。  
开头也说了，mac的shell版本是bash，还是很好使的，但是不足以让我们飞起来，我们要用的是zsh。可以使用 cat /etc/shells 看系统预装的shell。可以看到，mac下是预装了zsh的，省去了安装的麻烦。

zsh只能说是飞机，要飞起来还得有催化剂——oh my zsh。  
1、克隆 oh my zsh 到本地

`git clone git://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh`2、创建zsh 配置文件

`cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc`3、设置zsh默认shell

`chsh -s /bin/zsh`4、重启终端即可

环境变量、别名等全局终端的就可以写在 ~/.zshrc 中了，跟bash下的 ~/.bash\_profile 一个道理。

zsh 的主题在 ~/.oh-my-zsh/themes 目录下，可以修改配置文件中 ZSH\_THEME 的值选择自己想要的主题。

也可以参考这里：https://github.com/robbyrussell/oh-my-zsh/wiki/themes

就想vim一样，好用的不仅仅是工具本身，更重要的是插件。先说两个我比较喜欢的插件：autojump、incr(Incremental)。

安装autojump：brew install autojump

修改 .zshrc 配置文件，添加要使用的插件：plugins=(git autojump incr)

在 ~/.oh-my-zsh/custom/plugins 目录下创建 incr 目录，并在 incr 目录下创建 incr.plugin.zsh 配置文件，文件内容为：http://mimosa-pudica.net/src/incr-0.2.zsh

```

# Incremental completion for zsh
# by y.fujii , public domain

autoload -U compinit
zle -N self-insert self-insert-incr
zle -N vi-cmd-mode-incr
zle -N vi-backward-delete-char-incr
zle -N backward-delete-char-incr
zle -N expand-or-complete-prefix-incr
compinit

bindkey -M viins '^[' vi-cmd-mode-incr
bindkey -M viins '^h' vi-backward-delete-char-incr
bindkey -M viins '^?' vi-backward-delete-char-incr
bindkey -M viins '^i' expand-or-complete-prefix-incr
bindkey -M emacs '^h' backward-delete-char-incr
bindkey -M emacs '^?' backward-delete-char-incr
bindkey -M emacs '^i' expand-or-complete-prefix-incr

unsetopt automenu
compdef -d scp
compdef -d tar
compdef -d make
compdef -d java
compdef -d svn
compdef -d cvs

# TODO:
#     cp dir/

now_predict=0

function limit-completion
{
	if ((compstate[nmatches] <= 1)); then 		zle -M "" 	elif ((compstate[list_lines] > 6)); then
		compstate[list]=""
		zle -M "too many matches."
	fi
}

function correct-prediction
{
	if ((now_predict == 1)); then
		if [[ "$BUFFER" != "$buffer_prd" ]] || ((CURSOR != cursor_org)); then
			now_predict=0
		fi
	fi
}

function remove-prediction
{
	if ((now_predict == 1)); then
		BUFFER="$buffer_org"
		now_predict=0
	fi
}

function show-prediction
{
	# assert(now_predict == 0)
	if
		((PENDING == 0)) &&
		((CURSOR > 1)) &&
		[[ "$PREBUFFER" == "" ]] &&
		[[ "$BUFFER[CURSOR]" != " " ]]
	then
		cursor_org="$CURSOR"
		buffer_org="$BUFFER"
		comppostfuncs=(limit-completion)
		zle complete-word
		cursor_prd="$CURSOR"
		buffer_prd="$BUFFER"
		if [[ "$buffer_org[1,cursor_org]" == "$buffer_prd[1,cursor_org]" ]]; then
			CURSOR="$cursor_org"
			if [[ "$buffer_org" != "$buffer_prd" ]] || ((cursor_org != cursor_prd)); then
				now_predict=1
			fi
		else
			BUFFER="$buffer_org"
			CURSOR="$cursor_org"
		fi
		echo -n "\e[32m"
	else
		zle -M ""
	fi
}

function preexec
{
	echo -n "\e[39m"
}

function vi-cmd-mode-incr
{
	correct-prediction
	remove-prediction
	zle vi-cmd-mode
}

function self-insert-incr
{
	correct-prediction
	remove-prediction
	if zle .self-insert; then
		show-prediction
	fi
}

function vi-backward-delete-char-incr
{
	correct-prediction
	remove-prediction
	if zle vi-backward-delete-char; then
		show-prediction
	fi
}

function backward-delete-char-incr
{
	correct-prediction
	remove-prediction
	if zle backward-delete-char; then
		show-prediction
	fi
}

function expand-or-complete-prefix-incr
{
	correct-prediction
	if ((now_predict == 1)); then
		CURSOR="$cursor_prd"
		now_predict=0
		comppostfuncs=(limit-completion)
		zle list-choices
	else
		remove-prediction
		zle expand-or-complete-prefix
	fi
}

```

然后重启终端或者重新加载下配置文件即可。

当然，如果到现在你还没过瘾，还可以再安装iterm2，可以各种快捷键配置也是很爽的，也可以修改配色方案：http://ethanschoonover.com/solarized

不过我在oh my zsh 中已经选了自己中意的主题，对主题也没有特别的要求，就懒得再折腾了。

最后上一张我现在的主题图。

[![mac-zsh](/images/2016/01/mac-zsh.png)](/images/2016/01/mac-zsh.png)
