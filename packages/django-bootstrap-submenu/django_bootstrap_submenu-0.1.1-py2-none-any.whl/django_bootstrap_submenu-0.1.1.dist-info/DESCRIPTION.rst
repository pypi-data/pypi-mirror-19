###django-bootstrap-submenu
[bootstrap-submenu examples](https://vsn4ik.github.io/bootstrap-submenu/#html-examples)

###说明：

因为是bootstrap组件，所以jquery、bootstrap等推介使用：
jquery - pip install jquery
bootstrap - pip install bootstrap_themes
它们的使用方式和当前组件一样。

###安装指南
下载或者clone当前仓库，然后在项目目录中执行：
	python setup.py install

###使用指南：

```
settings.py
```
```
INSTALLED_APPS = (
'jquery',
'bootstrap_themes',
'bootstrap_submenu',
...
)
```

```
xxxx.html(模板文件使用)
```
```
{% load bootstrap_submenu%}
{% bootstrap_submenu_css%}
{% bootstrap_submenu_js%}
```

```
<div class="row">
  <div class="col-sm-4 col-sm-offset-2 m-b">
    <div class="dropdown">
      <button class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown" data-submenu>
        Dropdown <span class="caret"></span>
      </button>

      <ul class="dropdown-menu">
  <li class="dropdown-submenu">
  <a tabindex="0">Action</a>

  <ul class="dropdown-menu">
    <li><a tabindex="0">Sub action</a></li>
    <li class="dropdown-submenu">
      <a tabindex="0">Another sub action</a>

      <ul class="dropdown-menu">
        <li><a tabindex="0">Sub action</a></li>
        <li><a tabindex="0">Another sub action</a></li>
        <li><a tabindex="0">Something else here</a></li>
      </ul>
    </li>
    <li><a tabindex="0">Something else here</a></li>
    <li class="disabled"><a tabindex="-1">Disabled action</a></li>
    <li class="dropdown-submenu">
      <a tabindex="0">Another action</a>

      <ul class="dropdown-menu">
        <li><a tabindex="0">Sub action</a></li>
        <li><a tabindex="0">Another sub action</a></li>
        <li><a tabindex="0">Something else here</a></li>
      </ul>
    </li>
  </ul>
</li>
<li class="dropdown-header">Dropdown header</li>
<li class="dropdown-submenu">
  <a tabindex="0">Another action</a>

  <ul class="dropdown-menu">
    <li><a tabindex="0">Sub action</a></li>
    <li><a tabindex="0">Another sub action</a></li>
    <li><a tabindex="0">Something else here</a></li>
  </ul>
</li>
<li><a tabindex="0">Something else here</a></li>
<li class="divider"></li>
<li><a tabindex="0">Separated link</a></li>
</ul>

    </div>
  </div>
</div>
<script>
$(function(){
	$('[data-submenu]').submenupicker();//启动submenu组件
});
</script>
```


