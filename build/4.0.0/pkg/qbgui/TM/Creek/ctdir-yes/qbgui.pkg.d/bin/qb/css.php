/* /style/main begin */ 
@charset "utf-8";
/*!
 * AC 3.0.0
 * Copyright(c) 2006-2009 Sangfor, LLC
 * 样式复写
 * kangcheng
 * 2009-2010
 */
/* CSS Document */
a:link, a:visited {
	color: #0033CC;
	text-decoration: none;
}
a:hover,a:active {
	color:#0000FF;
	text-decoration:  underline;
}
/* IE8下a有泄漏，换用span模拟 by zz, at 2010/07/14 */
.sim-link{
	color: #0033CC;
	text-decoration: underline;
	cursor: pointer;
}
/*
 * 修正中文字体大小
 */
body {
	font-size: 12px;
}
div {
	font-size: 12px;
	font-family:arial;
}

.x-tip .x-tip-body {
	font: normal 12px  Arial;
    color:#444;
	table-layout:fixed;
	word-wrap:break-word;
	overflow:auto;
}
.x-toolbar td, .x-toolbar span, .x-toolbar input, .x-toolbar div, .x-toolbar select, .x-toolbar label,.x-btn button,.x-grid-group-hd div.x-grid-group-title,.x-grid3-hd-row td, .x-grid3-row td, .x-grid3-summary-row td,.x-list-body dt em {
	font: normal 12px  Arial;
}

/*覆盖所有已定义的字体大小,也可以对以下标签单独定义*/
dt, dd, li, td, span, em, select, input, button, a, b, p, pre, legend, label {
	font-size: 12px !important;
	font-family:arial;
}
/*
 * 框架主页面
 * 头部
 */
.head dl, .head dt, .head dd, .head ul, .head li {
	margin: 0px;
	padding: 0px;
	list-style: none;
}
.head {
	height: 55px;
	background: url(../images/top_bj.jpg) repeat-x;
	width: 100%;
	min-width: 500px;
 	/*_width: expression((document.documentElement.clientWidth||document.body.clientWidth)<1002?"1002px":"100%"); /*IE6*/
}
.head dl {
	height: 55px;
	background: url(../images/top_logo_bj.jpg) no-repeat left 0px;
}
.head dt {
	height: 35px;
	float: left;
	padding-top: 19px;
	padding-left: 170px;
	font-family: Verdana, Geneva, sans-serif;
}
.head dd {
	color:#FFF;
	height:55px;
	float: right;
	text-align:right;
	padding:0px 10px 0 0;
	background: url(../images/top_logo_bj.jpg) no-repeat right bottom;
}
.head dd ul {
	height: 22px;
	_float: left;
	margin-top:15px;
	padding:0px 0px 0px 20px;
	background:url(../images/top_right_bj.jpg) no-repeat left;
}
.head dd li {
	height: 22px;
	_float: left;
	line-height: 22px;
	padding:0px 10px 0px 0px;
	background: url(../images/top_right_bj.jpg) no-repeat right;
}
.head dd strong {
	color:#FFCC00;
	padding:0 5px 0 0;
	font-family: Verdana, Geneva, sans-serif;
}
.head dd span, .head dd span a {
	color:#DFDFDF;
	padding:0 5px;
}
.head a:link, .head a:visited {
	color: #E9E9E9;
	text-decoration: none;
}
.head a:hover, .head a:active {
	text-decoration: none;
	color: #FFCC3C;
}
.head strong {
	font-weight:bold;
}
/*
 * 框架主页面
 * 底部状态栏
 */
.copyright {
	height:25px;
	background: url(../images/Copyright_bj.gif) repeat-x;
	overflow: hidden;
	
}
.copyright dl {
	padding:0 10px;
	margin:0px;
	font: 11px Verdana, Geneva, sans-serif;
	color: #333;
}
.copyright dt {
	float: left;
	padding-top:6px;
}
.copyright dd {
	float: right;
	padding-top:6px;
}
.copyright dd span, .copyright dt {
	font-size:11px!important;
}
/*
 * 全局
 * 工具栏小图标
 */
.x-date-mp-ybtn a {
	background-image:url(../images/tool-sprites.gif)!important;
}
.x-tool {
	background-image:url(../images/tool-sprites.gif)!important;
}
.x-tree-arrows .x-tree-elbow-plus,
.x-tree-arrows .x-tree-elbow-minus,
.x-tree-arrows .x-tree-elbow-end-plus,
.x-tree-arrows .x-tree-elbow-end-minus {
	background-image:url(../images/arrows.gif)!important;
}
.left-menu .x-tree-arrows .x-tree-elbow-plus,
.left-menu .x-tree-arrows .x-tree-elbow-minus,
.left-menu .x-tree-arrows .x-tree-elbow-end-plus,
.left-menu .x-tree-arrows .x-tree-elbow-end-minus {
	background-image:url(../images/arrows_two.gif)!important;
	background-image:url(../images/arrows_two.gif)!important;
}
.x-tab-strip .x-tab-strip-closable a.x-tab-strip-close {
	background-image:url(../images/tab-close.gif);
}
.x-tab-strip .x-tab-strip-closable a.x-tab-strip-close:hover {
	background-image:url(../images/tab-close-hover.gif);
}
.x-tab-strip .x-tab-strip-active a.x-tab-strip-close {
	background-image:url(../images/tab-close-active.gif);
}
/*
 * 框架主页面
 * 左百叶窗菜单
 * headerCssClass : "left-menu-title",
 * bwrapCssClass : "left-menu",
 */
.x-tree-node{
	color:#000;
	font: normal 12px "arial"!important;
}
.left-menu-title {
	color:#fff!important;
	border: #3D64A0 1px solid!important;
	font-weight:bold!important;
	line-height: 17px!important;
	padding:6px 3px 4px 5px!important;
	background-image: url(../images/left-menu-title.gif)!important;
}
/**/

.left-menu-title .x-tool-collapse-west {
    background-position:0 -390px;
}
.left-menu-title .x-tool-collapse-west-over {
    background-position:-15px -390px;
}
/**/
.left-menu-title span {
	font-size:14px!important;
}
.left-menu .x-accordion-hd {
	background: url(../images/menu-bj.gif) repeat-x 0px -54px!important;
}
.left-menu .x-panel-collapsed .x-accordion-hd {
	background: url(../images/menu-bj.gif) repeat-x 0px 0px!important;
}
.left-menu .x-panel-collapsed .sf-nav-over {
	background: url(../images/menu-bj.gif) repeat-x 0px -27px!important;
}
.left-menu .x-accordion-hd {
	padding-top:6px!important;
	padding-bottom:4px!important;
	border-top:0 none;
	color:#283342;
	font-weight:bold;
}
.left-menu .x-panel-noborder .x-panel-collapsed .x-panel-header-noborder {
	border-bottom-color:#4C6488!important;
	border-top:1px solid #F6FBFE;
}
.left-menu .x-panel-noborder .x-panel-header-noborder {
	border-bottom-color:#708EB3!important;
	border-top:1px solid #fff;
}
.left-menu .x-tool {
	float:left!important;
}
.left-menu .x-panel-header {
	line-height: 16px;
	padding:5px 3px 4px 4px!important;
}
/**/
.left-menu .x-tree-node-leaf .x-tree-node-icon {
	background-image:none!important;
	display:none;
}
.left-menu .x-tree-node-leaf .x-tree-ec-icon {
	background-image:url(../images/menu-arrow.gif);
}
/**/
.left-menu .sf-nav-child .x-tree-node-icon, .left-menu .sf-nav-child .x-tree-ec-icon {
	
	background-image:url(../images/menu-arrow2.gif);
}
.left-menu .sf-nav-child .x-tree-node-indent .x-tree-elbow-line {
	background-image:none!important;
}
/**/
.left-menu .x-tree-node-expanded .x-tree-node-icon {
	background-image: none!important;
	display:none;
}
.left-menu .x-tree-node-collapsed .x-tree-node-icon {
	background-image:none!important;
	display:none;
}
/**/
.left-menu .x-tree-node .x-tree-node-leaf a {
	color: #061E64;
	font-weight: normal;
}
/**/
.left-menu .x-tree-node .x-tree-node-over a {
	color: #FF3300;
}
.left-menu .x-tree-node a span {
	color: #283342;
	font-weight: bold;
}
/**/
.left-menu .x-tree-node .x-tree-selected a {
	color: #FF3300;
	text-decoration:  none;
}
/**/
.left-menu .x-tree-node .sf-nav-root {
	padding-left:14px;
}
.left-menu .x-tree-node .x-tree-node-ct li .sf-nav-child {
	padding-left:8px;
}
/**/
.left-menu .x-tree-node-leaf .x-tree-ec-icon, .left-menu .x-tree-node-leaf .x-tree-elbow-line {
	border: 0 none;
	height: 18px;
	margin: 0;
	padding: 0;
	vertical-align: top;
	width: 16px;
	background-position:center;
	background-repeat: no-repeat;
}
/**/
.left-menu .x-panel-body {
	border-color:#4C6488;
	background-color:#E9F2FC!important;
}
/**/
.left-menu .x-tree-node-el {
	padding:3px;
}
.left-menu .sf-nav-root {
	padding:5px;
	background: url(../images/menu-x.gif) no-repeat left bottom!important;
}
.left-menu .x-tree-node .x-tree-node-ct {
	padding-bottom:10px;
	background: url(../images/menu-x.gif) no-repeat left bottom!important;
}
.left-menu .x-tree-node-expanded {
	background-image:none!important;
	padding:5px 5px 0px 5px;
}
/**/
.left-menu .x-tree-node .x-tree-node-over,.left-menu .x-tree-node .x-tree-selected  {
    background-color:#E9F2FC!important;
}
.left-menu .x-tree-arrows .x-tree-node-over .x-tree-elbow-plus,.left-menu .x-tree-arrows .x-tree-node-over .x-tree-elbow-end-plus{
    background-position:-32px 0!important;
}
.left-menu .x-tree-arrows .x-tree-node-over .x-tree-elbow-minus,.left-menu .x-tree-arrows .x-tree-node-over .x-tree-elbow-end-minus{
    background-position:-48px 0;
}
.left-menu .x-tree-node .x-tree-node-expanded a,.left-menu .x-tree-node .x-tree-node-collapsed a {
	color: #061E64!important;
}
/*
 * 框架主页面
 * 综合策略百叶窗菜单
 * headerCssClass : "left-menu-title-two",
 * bwrapCssClass : "left-menu-two",
 */

.left-menu-title-two {
	border: #708EB3 1px solid!important;
	font-weight:bold!important;
}
.left-menu-two .x-accordion-hd {
	background: url(../images/menu-bj.gif) repeat-x 0px -54px!important;
}
.left-menu-two .x-panel-collapsed .x-accordion-hd {
	background: url(../images/menu-bj.gif) repeat-x 0px 0px!important;
}
.left-menu-two .x-panel-collapsed .sf-nav-over {
	background: url(../images/menu-bj.gif) repeat-x 0px -27px!important;
}
.left-menu-two .x-accordion-hd {
	/*
 padding-top:6px!important;
 padding-bottom:4px!important;
*/
 border-top:0 none;
	color:#283342;
	font-weight:bold;
}
.left-menu-two .x-panel-noborder .x-panel-collapsed .x-panel-header-noborder {
	border-bottom-color:#4C6488!important;
	border-top:1px solid #F6FBFE;
}
.left-menu-two .x-panel-noborder .x-panel-header-noborder {
	border-bottom-color:#708EB3!important;
	border-top:1px solid #fff;
}
.left-menu-two .x-tool {
	float:left!important;
}
.left-menu-two .x-panel-header {
	/*
 line-height: 16px;
 padding:5px 3px 4px 4px!important;
*/
font-weight:normal;
	color:#000;
}
/**/
.left-menu-two .x-panel-body {
	border-color:#4C6488;
	background-color:#E9F2FC!important;
}
.left-menu-two .x-panel-body {
	border-color:#708EB3;/*border-bottom:1px solid #ACBDD2;*/
}
.left-menu-two .x-tool {
	width:15px;
}
.left-menu-two .x-tree-node-leaf .x-tree-node-icon {
	background-image:none;
	height: 0px;
	width: 0px;
}
/*

 * 框架主页面
 * 一级TAB页
 * cls:'sf-main-tab'
 */

.sf-main-tab {
	background-color: #C1DCF7;
	border-top-color:#284F8E;
	border-right-color:#284F8E;
	border-left-color:#284F8E;
	border-bottom-color:#5A76A5;
}
.sf-main-tab {
	padding-bottom: 3px;
}
.sf-main-tab ul.x-tab-strip-top {
	background-color:#cedff5;
	background-image: url(../images/tab-strip-bg.gif);
	border-bottom-color:#142854;
}
.sf-main-tab .x-tab-strip-top .x-tab-right, .sf-main-tab .x-tab-strip-top .x-tab-left, .sf-main-tab .x-tab-strip-top .x-tab-strip-inner {
	background-image: url(../images/tabs-sprite.gif);
}
.sf-main-tab .x-tab-strip span.x-tab-strip-text {
	font:normal 11px tahoma, arial, helvetica;
	color:#fff;
}
.sf-main-tab .x-tab-strip-active span.x-tab-strip-text {
	color:#0F2C72;
	font-weight:normal;
}
.sf-main-tab .x-tab-strip span.x-tab-strip-text {
	white-space: nowrap;
	cursor:pointer;
	padding:6px 0 2px 0;
	line-height:14px/*解决在IE下大写英文行高不一至导致撑开问题*/;
}
.sf-main-tab .x-tab-strip-top .x-tab-strip-active .x-tab-right span.x-tab-strip-text {
	padding-bottom:3px;
}
.sf-main-tab .x-tab-strip .x-tab-strip-closable a.x-tab-strip-close {
	opacity:.6;
	-moz-opacity:.6;
	filter:alpha(opacity=60);
	width:12px;
	height:12px;
	top:4px;
	right:3px;
}
主页面.sf-main-tab .x-tab-strip-closable .x-tab-left {
	padding-right:22px;
}
/*
 * 框架
 * Tab右侧按钮样式
 */
#sf_main_tabpanel .sf-main-tab-toolbar{
	background-color:#C1DCF7;
	border-width:1px 1px 1px 0;
	border-style:solid;
	border-color:#284F8E #284F8E #5A76A5;
	padding:0 0 3px 0;
}
#sf_main_tabpanel .sf-main-tab-toolbar .x-toolbar{
	/*height:23px!important;*/
	padding:1px 0 0 0;
	border-width:0 0 1px 0;
	border-color:#142854;
	border-style:solid;
	background-image:url("../images/tab-strip-bg.gif");
	background-repeat:repeat-x;
	background-position:50% 100%;
}
/*ExtJs 3.x中的TabPanel，在IE8(Q)下标签栏高了1象素，导致错位。这里同步增高以保持一致*/
.ext-border-box .ext-ie8 #sf_main_tabpanel .sf-main-tab-toolbar .x-toolbar{
	padding-top:2px;
}
/* 英文版文字高度不一样，这里加上overflow防止首页工具栏错位 */
#sf_main_tabpanel .sf-main-tab-toolbar .x-toolbar .x-btn button{
	overflow: hidden;
}
/*把以前的Tab栏右边框去掉，实现无缝拼接*/
#sf_main_tabpanel .x-tab-panel-header{
	border-right-width:0px;
}
/*
 * 框架主页面
 * 二级TAB页
 * cls:'sf-two-tab'
 */
.sf-two-tab .x-tab-panel-header {
	background-color: #BEDBF5;
	padding-bottom: 0px;
	border-top:#4C6488 solid 1px;
	border-right:#4C6488 solid 1px;
	border-left:#4C6488 solid 1px;
	border-bottom:0 none;
	
}
.sf-two-tab ul.x-tab-strip-top {
	background-color:#cedff5;
	background-image: url(../images/window-tab-strip-bg.gif);
	border-bottom-color:#4C6488;
}
.sf-two-tab .x-tab-strip-top .x-tab-right, .sf-two-tab .x-tab-strip-top .x-tab-left, .sf-two-tab .x-tab-strip-top .x-tab-strip-inner {
	background-image: url(../images/window-tabs-sprite.gif);
}
.sf-two-tab .x-tab-strip span.x-tab-strip-text {
	font:normal 12px tahoma, arial, helvetica;
	color:#333;
}
.sf-two-tab .x-tab-strip-active span.x-tab-strip-text {
	color:#000;
	font-weight:normal;
}
.sf-two-tab .x-tab-strip span.x-tab-strip-text {
	white-space: nowrap;
	cursor:pointer;
	padding:6px 0 2px 0;
	line-height:14px/*解决IE下有大写或符号的TAB撑开TAB标签BUG*/;
}
.sf-two-tab .x-tab-strip-top .x-tab-strip-active .x-tab-right span.x-tab-strip-text {
	padding-bottom:3px;
}
.sf-two-tab .x-tab-strip .x-tab-strip-closable a.x-tab-strip-close {
	opacity:.6;
	-moz-opacity:.6;
	filter:alpha(opacity=60)/*解决IE下BUG*/;
	width:12px;
	height:12px;
	top:4px;
	right:3px;
}
.sf-two-tab .x-tab-panel-body {
	border-color:#708EB3;
	background-color:#ECF5FD;
}
/*
 * 二级TAB页 无边框背景
 * cls:'sf-two-tab-none'
 */
.sf-two-tab-none .x-tab-panel-header {
	background-color: #BEDBF5;
	border: none;
	padding-bottom: 0px;
}
.sf-two-tab-none ul.x-tab-strip-top {
	background:none!important;
	background-image: url(none)!important;
}
.sf-two-tab-none .x-tab-panel-header {
	background:none!important;
}
.sf-two-tab-none .x-tab-strip-active span.x-tab-strip-text {
	font-weight:bold!important;
}
/*panel背景*/
.sf-two-tab-none .x-panel-body {
	background-color:#F1F6FB;
}
/*
 * 框架主页面
 * 一级TITLE
 */
.x-panel-header {
	color:#0F2C72;
	font-weight:bold;
	font-size: 12px;
	font-family: tahoma, arial, verdana, sans-serif;
	border-color:#708EB3;
	background-image: url(../images/white-top-bottom.gif);
}
.x-panel-noborder .x-panel-header-noborder {
    border-bottom-color:#708EB3;
}
/*
 * 弹出窗口
 * 全局(window)
 */
.x-window .x-tool {
	width:18px;
}
.x-window-bwrap .x-tab-panel-body {
	border-color:#4C6488;
	background-color:#F3F8FC;
}
.x-window-tl .x-window-header {
	padding:6px 0 7px 0!important;
	color:#F4F7FC;
	background: url(../images/window/right-bj.png) no-repeat right top;
}
/*解决在IE下大写英文行高不一至导致撑开问题*/
.ext-ie .x-window-tl .x-window-header {
	height:30px;
	padding:8px 0 0 0!important;
}
/**/
.x-window-tl .x-window-header .x-window-header-text {
	font-size:14px!important;
	font-weight:bold;
	display:block;
	overflow:hidden; 
	white-space:nowrap; 
	text-overflow:ellipsis;
}
.ext-ie .x-window-tl .x-window-header .x-window-header-text {
	width:90%;
}
.x-window-maximized .x-window-tc {
	background-color:#fff;
}
.x-window-bc .x-window-footer {
	padding-bottom:3px;
	zoom:1;
	font-size:0;
	line-height:0;
}
.x-window-ml {
	padding-left:1px;
}
.x-window-mr {
	padding-right:1px;
}
.x-window-bl {
	padding-left:1px;
}
.x-window-br {
	padding-right:1px;
}
.x-window-tl {
	background: transparent no-repeat 0 0;
	padding-left:6px;
	zoom:1;
	z-index:1;
	position:relative;
}
.x-window-tr {
	background: transparent no-repeat right 0;
	padding-right:6px;
}
.x-window-tc {
	background-image: url(../images/window/top-bottom.png);
}
.x-window-tl {
	background-image: url(../images/window/left-corners.png);
}
.x-window-tr {
	background-image: url(../images/window/right-corners.png);
}
.x-window-bc {
	background-image: url(../images/window/top-bottom.png);
}
.x-window-bl {
	background-image: url(../images/window/left-corners.png);
}
.x-window-br {
	background-image: url(../images/window/right-corners.png);
}
.x-window-mc {
	border-color:#99bbe8;
	font: normal 11px tahoma, arial, helvetica, sans-serif;
	background-color:#dfe8f6;
}
.x-window-ml {
	background-image: url(../images/window/left-right.png);
}
.x-window-mr {
	background-image: url(../images/window/left-right.png);
}
.x-window-bl .x-btn button {
	color:#000;
}
/*
 * 弹出窗
 * TITLE
 * cls:'sf-window-panel',
 */
.sf-window-panel .x-panel-header {
	font-size: 14px;
	font-family: tahoma, arial, verdana, sans-serif;
	border-color:#8DA2BB;
	background-color:#ECF2FA;
	background-image:url(../images/window_title.gif);
	color:#333;
}
/*
 * 弹出窗
 * 二级TAB页
 * cls:'window_tab_two'
 */
.window_tab_two ul.x-tab-strip-top {
	background:none!important;
	background-image: url(none)!important;
}
.window_tab_two .x-tab-panel-header {
	background:none!important;
}
.window_tab_two .x-tab-strip-active span.x-tab-strip-text {
	font-weight:bold!important;
}
/*panel背景*/
.window_tab_two .x-panel-body {
	background-color:#F1F6FB;
}
/*
 * 弹出窗口
 * TAB
 */
.x-window .x-tab-panel-header {
	background-color: #BEDBF5;
	border: none;
	padding-bottom: 0px;
}
.x-window ul.x-tab-strip-top {
	background-color:#cedff5;
	background-image: url(../images/window-tab-strip-bg.gif);
	border-bottom-color:#4C6488;
}
.x-window .x-tab-strip-top .x-tab-right, .x-window .x-tab-strip-top .x-tab-left, .x-window .x-tab-strip-top .x-tab-strip-inner {
	background-image: url(../images/window-tabs-sprite.gif);
}
.x-window .x-tab-strip span.x-tab-strip-text {
	font:normal 12px tahoma, arial, helvetica;
	color:#333;
}
.x-window .x-tab-strip-active span.x-tab-strip-text {
	color:#0F2C72;
	font-weight:normal;
}
.x-window .x-tab-strip span.x-tab-strip-text {
	white-space: nowrap;
	cursor:pointer;
	padding:6px 0 2px 0;
	line-height:14px/*解决IE下有大写或符号的TAB撑开TAB标签BUG*/;
}
.x-window .x-tab-strip-top .x-tab-strip-active .x-tab-right span.x-tab-strip-text {
	padding-bottom:3px;
}
.x-window .x-tab-strip .x-tab-strip-closable a.x-tab-strip-close {
	opacity:.6;
	-moz-opacity:.6;
	filter:alpha(opacity=60)/*解决IE下BUG*/;
	width:12px;
	height:12px;
	top:4px;
	right:3px;
}
/*
 * 弹出窗口
 * toolbar
 */
.x-window .x-tab-panel .x-toolbar {
	border-color:#8DA2BB;
	background-color:#ECF2FA;
	background-image:url(../images/window_toolbar_bg.jpg);
}
/*toolbar*/
.x-panel-bbar .x-toolbar, .x-panel-tbar .x-toolbar {
	border-left-color:#708EB3;
	border-right-color:#708EB3;
	border-bottom-color:#9EB3CB;
}
.x-toolbar {
	border-color:#a9bfd3;
	background-color:#d0def0;
	background-image:url(../images/toolbar/bg.gif);
}
.x-panel-noborder .x-panel-tbar-noborder .x-toolbar {
	border-bottom-color:#6984AB;
}
.window-tool-bottom {
	border-bottom:none !important;
	border-top:#8DA2BB solid 1px !important;
}
.window-tool-bottom .x-toolbar-left {
	padding-left:5px;
}
.window-tool-bottom .x-form-checkbox {
	padding:0 2px;
}
.sf-searchtextarea .x-toolbar{
	border-color:#708EB3;
	background-color:#EDF4FC;
	background-image:none;
}
.sf-searchtextarea .x-form-field  {
	background-image:none;
}
/*
 * 弹出窗口
 * grids
 */
.window-grids {
	border:solid 1px #ABBDD3;
}
.window-grids .x-toolbar {
	border-color:#8DA2BB;
	background-color:#ECF2FA;
	background-image:url(../images/white-grids-toolbar.gif)!important;
	padding:1px 0;
}
.window-grids .x-grid3-row-selected {
	background-color: #F7FAFD !important;
	border-color:none!important;
	border-bottom-color:none!important;
	border-bottom:solid 1px #EDEDED !important;
	border-top:solid 1px #fff !important;
}
.window-grids .x-grid3-hd-inner {
	color:#333
}
.window-grids .x-grid3-td-checker {
	background-image:none!important;
}
.window-grids .x-panel-tbar-noborder .x-toolbar {
	border-bottom-color:#ABBDD3;
}
/*
 * 框架主页面
 * 定位菜单（纵向TAB）
 */
.menu-bg {
	background-color:#CBDEF3;
	padding:5px 3px 5px 5px!important;
	/*
	margin:5px!important;
	border:#98B1D1 solid 1px;
	
	position:absolute;*/
}
/*.menu-left {
	margin:0 -1 2px 0 !important;
	position:relative;
	float:left;
}*/
/* 默认 */
.menu-left .menu-view-item {
	background-color:#D8E6F6;
	border-right:#98B1D1 solid 1px;
	border-top:#C2D9F1 solid 1px;
	border-left:#C2D9F1 solid 1px;
	border-bottom:#C2D9F1 solid 1px;
	padding:5px 5px 5px 18px !important;
	margin:0 0 2px 0!important;
}

/* 激活 */
.menu-left .menu-view-selected {
	background-color:#FCFDFE!important;
	color:#000!important;
	border-top:#98B1D1 solid 1px;
	border-left:#98B1D1 solid 1px;
	border-bottom:#98B1D1 solid 1px;
	border-right:none;
	left:0px;
	top:0px
}
/* 悬停 */
.menu-left .menu-view-over {
	background-color:#E6EFF9;
}
.menu-right {
	background-color:#FCFDFE;
	border:#98B1D1 solid 1px;
}
/*全局，无背景*/
.background_none{
	background:none!important;
}
/*
 * 框架主页面
 * formpage
 */
.x-formpage-wraped {
	padding:10px;
}
.x-formpage {
	border:#6B91BE solid 1px;
	background:#E7F2FC;
}
.x-formpage-header {
	margin:0 6px;
	color: #666;
	font-size:14px!important;
	padding:20px 14px 14px 45px;
	border-bottom: 2px solid #D9E2E9;
	background: url(../images/xd_title.png) no-repeat left;
}
.x-formpage-header spanspan {
	font-size:14px!important;
}
.x-formpage-bwrap {
	padding:0px;
}
.x-formpage-body {
/*
padding-left:38px;
*/
}
.x-formct {
	padding:10px/*这里不要改*/
}
.x-formct-fit {
	padding:0px!important;
}
.x-formpage-footer {
	padding:5px 20px;
}
.x-formpage-footer {
	/*
 background:no-repeat left top ;
 background-image:url(../images/button/button-top-x.gif);
*/

 border-top: 1px solid #B7C1D0;
}
.x-formpage-footer .x-btn .x-btn-tl, .x-formpage-footer .x-btn .x-btn-tr, .x-formpage-footer .x-btn .x-btn-tc, .x-formpage-footer .x-btn .x-btn-ml, .x-formpage-footer .x-btn .x-btn-mr, .x-formpage-footer .x-btn .x-btn-mc, .x-formpage-footer .x-btn .x-btn-bl, .x-formpage-footer .x-btn .x-btn-br, .x-formpage-footer .x-btn .x-btn-bc {
	background-image:url(../images/button/btn.gif);
}
.x-formpage-footer .x-btn-noicon .x-btn-small .x-btn-text {
	height:21px;
}
/*
 * 框架主页面
 * 部署模式
 * 建立在formpage样式上扩展
 */
.sf-DeployMode .x-tab-panel-body {
	border-color:#4C6488;
	background-color:#ECF5FD;
}
.sf-DeployMode ul.x-tab-strip-top {
	background-color:#cedff5;
	background-image: url(../images/sf-DeployMode-title.gif);
	border-bottom-color:#4C6488;
}
/**/
.sf-DeployMode td,.sf-DeployMode th,.sf-DeployMode div{
	font-family:"arial", Arial!important;
}
.sf-DeployMode .x-panel-body {
	background:none;
	border:none;
}
.sf-DeployMode .x-formpage-footer {
/*
 border-top: none;
*/
}
.sf-DeployMode .x-formpage-body {
	background-color:#E7F2FC!important;
}
.sf-DeployMode .x-formpage-header {
	font-size:20px!important;
}
.sf-DeployMode .x-formpage-header span {
	font-size:14px!important;
	font-weight:bold;
}
.sf-DeployMode-title {
	font-size:16px;
}
/*HOME*/
.sf-DeployMode-title{
	color:#283342;
	font-size:12px;
	font-family:Verdana, Geneva, Arial, Helvetica, sans-serif!important;
	font-weight:bold;
	padding:5px;
}
.sf-DeployMode-Home {
	color:#333;
}
.sf-DeployMode-NAT{
	border:#4C6488 solid 1px;
	background-color:#F1F6FB;
}
.sf-DeployMode-content{
	margin:5px 0px 5px 5px;
}
.sf-DeployMode-content th,.sf-DeployMode-content td{
	padding:2px 1px 2px 1px;
}
.sf-DeployMode-content th{
	text-align:left;
	color:#666;
}
/*
 * 从左到右引用组件
 * cls:'fieldset-panel',
 */
.fieldset-panel .x-panel-header {
	color:#333;
	font-weight:normal;
	font-size: 14px;
	border:none;
	border-bottom:#708EB3 solid 1px;
	background-image: url(none);
	padding-left:0px;
}
.ext-ie .fieldset-panel .x-list-body {
    overflow:auto;
    overflow-x:hidden;
    overflow-y:auto;
    zoom:1;
    float: left;
 /*
	width:auto;/*BUG 20463/
 */
}
/*window下*/
.x-window .fieldset-panel .x-panel-header, .x-window .fieldset-panel .x-table-layout-cell {
	background-color:#DFE8F6;
}
/*fieldset下*/
.x-fieldset .fieldset-panel .x-panel-header, .x-fieldset .fieldset-panel .x-table-layout-cell {
	background-color:#F1F6FB;
}
/*部署模式下*/
.sf-DeployMode .x-fieldset .fieldset-panel .x-panel-header, .sf-DeployMode  .x-fieldset .fieldset-panel .x-table-layout-cell {
	background-color:#E7F2FC;
}
.sf-DeployMode .fieldset-panel .x-panel-body {
	background:#fff;
	border:1px solid #708EB3;
}
.sf-DeployMode .fieldset-panel .x-panel-header {
	border-bottom:none;
}
.sf-DeployMode .fieldset-panel .x-list-selected {
	background-color:#E0EEFC;
}
.sf-DeployMode th{
	font-size:12px;
	font-family:Arial;
}
.sf-DeployMode .x-fieldset .x-fieldset-bwrap{
	padding-left:30px;
}
/*TAB下背景*/
.sf-DeployMode .sf-two-tab .x-tab-panel-body {
	background-color:#F1F6FB;
}
/*
/*部署模式
*/
.sf-help-html{
	color:#666;
	border-top:#ccc 1px solid;
	width:80%;
	margin-top:10px;
}
.sf-help-html p{
	padding:5px 0;
}
.sf-help-html span{
	color:#999;
	padding:3px 0;
	display:block;
}
/*
 * 框架主页面
 * 按钮
 */
.x-btn .x-btn-tl, .x-btn .x-btn-tr, .x-btn .x-btn-tc, .x-btn .x-btn-ml, .x-btn .x-btn-mr, .x-btn .x-btn-mc, .x-btn .x-btn-bl, .x-btn .x-btn-br, .x-btn .x-btn-bc {
	background-image:url(../images/button/btn.gif);
}
.Button-bg-none .x-btn .x-btn-tl, .Button-bg-none .x-btn .x-btn-tr, .Button-bg-none .x-btn .x-btn-tc, .Button-bg-none .x-btn .x-btn-ml, .Button-bg-none .x-btn .x-btn-mr, .Button-bg-none .x-btn .x-btn-mc, .Button-bg-none .x-btn .x-btn-bl, .Button-bg-none .x-btn .x-btn-br, .Button-bg-none .x-btn .x-btn-bc {
	background-image:none;
}
.Button-bg-none{
	display:inline-block;
	vertical-align:middle;
}
.ext-ie .Button-bg-none{
	display : inline;
	vertical-align:middle;
}
.x-row-editor .x-btn .x-btn-tl, .x-row-editor .x-btn .x-btn-tr, .x-row-editor .x-btn .x-btn-tc, .x-row-editor .x-btn .x-btn-ml, .x-row-editor .x-btn .x-btn-mr, .x-row-editor .x-btn .x-btn-mc, .x-row-editor .x-btn .x-btn-bl, .x-row-editor .x-btn .x-btn-br, .x-row-editor .x-btn .x-btn-bc {
	background-image:url(../images/button/btn_1.gif);
}
/*
 * 分组
 */
.sf-forms-panel{
	background-color:#E9F2FC;
	border:1px solid #CCD2DD ;
}
.sf-forms-panel .x-panel-body-noborder{
	background-color:#E9F2FC;
}
/* 分组按钮 */
.Button-top {
	border-top: 1px solid #CCD2DD;
}
.Button-bg {
	height:24px;
	border-left:#6984AB solid 1px;
	border-right:#6984AB solid 1px;
	border-bottom:#6984AB solid 1px;
	background-image:url(../images/button/Button-bg.jpg);
}
.ext-ie .Button-bg {
	height:34px;
}
/*toolbar按钮*/
.x-toolbar .x-btn-tl, .x-toolbar .x-btn-tr, .x-toolbar .x-btn-tc, .x-toolbar .x-btn-ml, .x-toolbar .x-btn-mr, .x-toolbar .x-btn-mc, .x-toolbar .x-btn-bl, .x-toolbar .x-btn-br, .x-toolbar .x-btn-bc {
	background-image:url(../images/button/btn_jiu.gif);
}
/*有checknone的toolbar按钮*/
.x-toolbar .sf-button-no-bg .x-btn-tl,
.x-toolbar .sf-button-no-bg .x-btn-tr, 
.x-toolbar .sf-button-no-bg .x-btn-tc, 
.x-toolbar .sf-button-no-bg .x-btn-ml, 
.x-toolbar .sf-button-no-bg .x-btn-mr, 
.x-toolbar .sf-button-no-bg .x-btn-mc, 
.x-toolbar .sf-button-no-bg .x-btn-bl, 
.x-toolbar .sf-button-no-bg .x-btn-br, 
.x-toolbar .sf-button-no-bg .x-btn-bc {
	background-image:none;
}
.x-btn-over .sf-ico-checknone {
    background-image: url(../images/default/tree/checknone_hover.gif) !important;
}
.x-btn-over .sf-ico-checkall {
    background-image: url(../images/default/tree/checkall_hover.gif) !important;
}
/*
 * 组件
 * 设置条件信息预览、加速选项磁盘缓存
 */
.x-panel-filter-key {
	padding:7px 10px;
	background:#D0E4F9;
	border-bottom:#6984AB solid 1px;
}
/*
 * 组件
 * 刷新间隔
 */
.x-menu-list-item, .x-menu-border-item, .x-menu-item .x-panel-body {
	background:none!important;
}
/*解决无法双击选择*/
.sf-menu-list-item-custom,.sf-menu-list-item-custom .x-menu-list-item {
-moz-user-select:-moz-none;
}

/*
 * 组件
 * 简单选择器
 */
.GeneralSelector {
	background:none!important;
}
.GeneralSelector .x-toolbar {
	border-color:#708EB3;
}
.sf-ellipsis tr:hover {
	background-color:#EEEEEE;
}
.sf-ellipsis td {
	height:22px;
	padding:0 3px 0 3px;
	border-bottom:#EEEEEE solid 1px;
}
.sf-ellipsis div {
	white-space:nowrap;
	-o-text-overflow: ellipsis;    /* for Opera */
	text-overflow:ellipsis;        /* for IE */
	overflow:hidden;
	width:145px;
	display:block;
	float:left;
}
/*
 * 模板
 * 用户管理基本信息
 */
.sf-Basic-Info {
	border-bottom:1px solid #8CA5C3;
	background-color:#E4EFFC;
}
.sf-Basic-Info .x-panel-body {
	background-color:#DAE9FA;
}
.group-edit-link {
	padding:5px 10px;
	text-align:right;
}
.sf-flow td {
	white-space: nowrap;
}
/**/
.sf-table {
 table-layout:fixed;
 width: 95%;
 height: auto;
}
.sf-table td {
 text-overflow:ellipsis;
 white-space: nowrap;
 overflow: hidden;
 padding:1px;
}

/*
 * 框架主组件
 * grid3
 */
.x-grid3 {
	background-color:#F7FAFD;
}
.x-grid3-row-alt {
	background-color:#fff;
}
.x-grid3-row-over {
    background-color:#efefef!important;
}
/*
 * 框架主页面
 * 背景色
 */
.x-panel-body {
	border-color:#708EB3;
	background-color:#F7FAFD;
}
.x-tab-panel-body {
	border-color:#4C6488;
	background-color:#ECF5FD;
}
.x-border-layout-ct { 
	background-color:#97C2EE;
}
.x-tab-panel .x-border-layout-ct {
	background-color:#ECF5FD;
}
.x-window-body .x-border-layout-ct {
	background:none;
}
/*
 * 左菜单收缩
 */
.x-layout-collapsed {
	background-color:#5E95D9;
	border-color:#284F8E;
}
.x-tab-panel-bwrap .x-layout-collapsed {
	background-color:#D9E8FB;
	border-color:#708EB3;
}
.x-tab-panel-bwrap .x-layout-collapsed-over {
	background-color:#C1DCF8;
	border-color:#708EB3;
}
.x-tab-panel-bwrap .x-tool-expand-west {
    background-position:0 -375px;
}

.x-tab-panel-bwrap .x-tool-expand-west-over {
    background-position:-15px -375px;
}

/*
 * 时间计划组
 */
.sf-TimePlan{
	background:none!important;
}
.sf-TimePlan .x-panel-header {
	color:#000;
	font-weight:normal;
	border-color:#8DA2BB;
	background-image:url(../images/white-grids-toolbar.gif)!important;
}
.sf-TimePlan .time-select-inner{
	background-color:#F9F9F9;
}
.sf-TimePlan .x-grid3-header{
	padding:0;
}
.sf-TimePlan .sf-TimePlan-x .x-grid3-header-offset{
	border-left:#c1c1c1 1px solid ;
	padding-left:0px;
}
.sf-TimePlan .sf-TimePlan-y .x-grid3-header-offset{
	padding:1px;
}
/*
 * 应用特征识别库
 */
.sf-appidentifyrule .x-grid3-row td, .sf-appidentifyrule-grids .x-grid3-summary-row td {
	vertical-align:inherit;
}
.sf-appidentifyrule .x-grid3-body .x-grid3-td-checker,.checker-no-bg .x-grid3-body .x-grid3-td-checker {
    background-image: url(none);
}
.sf-appidentifyrule .sf-button,.rounded .sf-button{
	background:url(../images/sf_button.gif);
	border:0px solid;
	width:66px;
	height:22px;
	cursor:pointer;
}
.ext-ie .sf-appidentifyrule .x-grid3-body .x-grid3-td-checker .x-grid3-cell-inner{
    padding:0 !important;
	height:auto;
}

.sf-appidentifyrule-title dt{
	float:left;
	padding-right:5px;
}
.sf-appidentifyrule-title dd{
	float:left;
}
.sf-appidentifyrule-title dd span{
	display:block;
	padding-top:3px;
}
.sf-appidentifyrule-title dt img{
	vertical-align:middle;
}

/*
 * 运行状态-资源信息
*/
.sf-sysstatus p {
	margin-top:8px;
}
.sf-x-160 {
	width:1px;
	background-image: url(../images/x-160.gif);
	background-repeat: no-repeat;
	background-position: center;
}
.collect-log th {
	border-bottom:#CCC solid 1px;
	font-weight:normal;
	font-size:12px;
	padding:3px;
	text-align:left;
}
.collect-log td {
	padding:6px 3px 0 3px;
}
/*
 * 冒泡信息
*/

.sf-news {
	table-layout:fixed;
	word-wrap:break-word;
}
.sf-news a{
	padding:3px;
	cursor:pointer;
}

.sf-news-paging span{
	padding:5px;
}
.sf-news-content{
	padding:10px 5px;
	border-bottom:#D4D5D7 solid 1px;
}
.sf-news-no-content{
	padding:5px;
	color:#F30;
}
/*屏蔽*/
.sf-news .sf-news-left{
	height:20px;
	vertical-align:middle;
}
.sf-news .sf-news-left div{
	float:left;
	margin:1px 3px 0 3px;
}
.sf-news .sf-news-left label{
	float:left;
}
.ext-ie .sf-news .sf-news-left div{
	margin:0px;
}
.ext-ie .sf-news .sf-news-left label{
	margin-top:5px;	
	padding-left:0px;
}
/**/
.sf-tip .x-tip-tc,
.sf-tip .x-tip-tl, .sf-tip .x-tip-tr,
.sf-tip .x-tip-bc, .sf-tip .x-tip-bl,
.sf-tip .x-tip-br, .sf-tip .x-tip-ml,
.sf-tip .x-tip-mr {
	background-image: url(../images/qtip/tip-sprite.gif);
}
.sf-tip .x-tip-anchor {
    background-image:url(../images/qtip/tip-anchor-sprite.gif);
}
.x-tip .x-tool-close {
    background-position:0 -405px;
}
.x-tip .x-tool-close-over {
    background-position:-15px -405px;
}
/*
 * 网口
*/
 .sf-NFBridgeConfig .x-grid3-row td,
 .sf-NFBridgeConfig .x-grid3-summary-row td,
 .sf-upper-center .x-grid3-row td,
 .sf-upper-center .x-grid3-summary-row td {
	vertical-align:inherit;
}
/*
 * 用户流量排行与应用流量排行 浮动层
*/
.floatingContent{
	 table-layout:fixed;
	 width:100%
}
.floatingContent th{
	font-size:12px;
	text-align:right;
	color:#666;
	padding:3px 5px;
	border-bottom:1px solid #ccc;
}
 .floatingContent td{
	color:#000;
	padding:5px;
	text-align:right;
	text-overflow:ellipsis;
	white-space: nowrap;
	overflow: hidden;
}
/*
 * 框架主页面
 * 面版背景色
 */
/*二级面/整体背景*/
.two-panel .x-border-layout-ct {
	background-image:none!important;
}
.two-panel .x-panel-body {
	background-color:#E0ECFA!important;
}
/*二级面版/西面背景*/
.two-west .x-panel-body {
	background-color:#EDF4FC!important;
}
/*二级面版/表格背景*/
.two-grid .x-grid3 {
	background-color:#F7FAFD!important;
}
/*
 * 超出隐藏部分（公共）
 */
.ellipsis{
	overflow:hidden; 
	white-space:nowrap; 
	text-overflow:ellipsis; /* for IE */ 
	-o-text-overflow: ellipsis; /* for Opera */ 
	-icab-text-overflow: ellipsis; /* for iCab */ 
	-khtml-text-overflow: ellipsis; /* for Konqueror Safari */ 
	-moz-text-overflow: ellipsis; /* for Firefox,mozilla */ 
	-webkit-text-overflow: ellipsis; /* for Safari,Swift*/ 
}
/*
 * 多告警信息组件
 */
.sf-multi-msgbox-brief{
	padding:5px;
}
.sf-multi-msgbox-list{
	margin:5px 5px 3px 5px;
	border:solid 1px #B4BFD1;
	background-color:#ffffff;
	overflow-y:scroll;
}
.sf-multi-msgbox-single .sf-multi-msgbox-list{
	margin:5px 5px 3px 5px;
	border:none;
	background:none;
	overflow-y:visible;
}
.sf-multi-msgbox-single .sf-multi-msgbox-brief{
	display:none;
}
.sf-multi-msgbox-item{
	padding: 10px 0;
	margin: 0 5px;
	border-bottom:solid 1px #ccc;
}
.sf-multi-msgbox-item-last{
	border:none;
	margin-bottom:5px;
}
.sf-multi-msgbox-icon {
	height:25px;
	width:25px;
	float:left;
}
.sf-multi-msgbox-single .sf-multi-msgbox-icon {
	height:40px;
	width:40px;
}
.sf-multi-msgbox-content{
	margin-left:30px;
	line-height:20px;
	word-wrap:break-word;
}
.sf-multi-msgbox-single .sf-multi-msgbox-content{
	margin-left:45px;
}
/*信息*/
.sf-multi-msgbox-item-info .sf-multi-msgbox-icon{
	background:url(../images/info02.gif) no-repeat;
	
}
/*错误*/
.sf-multi-msgbox-item-error .sf-multi-msgbox-icon{
	background:url(../images/error02.gif) no-repeat;
	
}
/*告警*/
.sf-multi-msgbox-item-warn .sf-multi-msgbox-icon{
	background:url(../images/alert02.gif) no-repeat;
	
}
/**/
.sf-multi-msgbox-single .sf-multi-msgbox-item-info .sf-multi-msgbox-icon{
	background:url(../ext/resources/images/default/window/icon-info.gif) no-repeat;
}
.sf-multi-msgbox-single .sf-multi-msgbox-item-error .sf-multi-msgbox-icon{
	background:url(../ext/resources/images/default/window/icon-error.gif) no-repeat;
}
.sf-multi-msgbox-single .sf-multi-msgbox-item-warn .sf-multi-msgbox-icon{
	background:url(../ext/resources/images/default/window/icon-warning.gif) no-repeat;
}

/*
 * 插件安装页面
 */
.rounded { margin-top:25%; }
.rounded .install { background: #EFEFEF url(../images/large-loading.gif) no-repeat; line-height: 32px; height:32px; padding-left: 45px!important; }
.rounded .al { display:block; text-align:right; padding:20px 0 0 0; }
/**/
.rounded .l-t { height: 10px; width: 10px; background: url(../images/rounded.gif) no-repeat 0px 0px; }
.rounded .z-t { background: url(../images/rounded.gif) 0px -20px; }
.rounded .r-t { height: 10px; width: 10px; background: url(../images/rounded.gif) no-repeat -10px 0px; }
/**/
.rounded .l-z { background: url(../images/rounded_2.gif) -10px 0px; }
.rounded .z-z { background-color: #EFEFEF; padding:0px 20px 3px 5px; font-size:12px; }
.rounded .r-z { background: url(../images/rounded_2.gif) 0px 0px; }
/**/
.rounded .l-b { height: 10px; width: 10px; background: url(../images/rounded.gif) no-repeat 0px -10px; }
.rounded .z-b { background: url(../images/rounded.gif) 0px -30px; }
.rounded .r-b { height: 10px; width: 10px; background: url(../images/rounded.gif) no-repeat -10px -10px; }
/**/
/*!
 * AC 3.0.0
 * Copyright(c) 2006-2009 Sangfor, LLC
 * 运行状态
 */
.x-portal .x-panel-dd-spacer {
 margin-bottom:10px;
}
.x-portlet {
 margin-bottom:10px;
}

/*有阴影效果
.x-portlet           portal默认样式
.x-panel-ghost       鼠标拖动portal时效果样式
.x-panel-collapsed   portal收缩后样式
*/
.x-portlet .x-panel-tc, .x-panel-ghost .x-panel-tc {
 background-image: url(../images/portlet/top-bottom.gif)!important;
}
.x-portlet .x-panel-bc {
 background-image: url(../images/portlet/top-bottom.gif)!important;
}
.x-portlet .x-panel-tl, .x-portlet .x-panel-tr,.x-panel-bl, .x-panel-br  {
 background-image: url(../images/portlet/corners-sprite.gif)!important;
}
.x-panel-ghost .x-panel-tl, .x-panel-ghost .x-panel-tr,.x-panel-bl, .x-panel-br  {
 background-image: url(../images/portlet/corners-sprite3.gif)!important;
}
.x-portlet .x-panel-mc {
 font: normal 11px tahoma, arial, helvetica, sans-serif;
 background-color:#F3F8FC;
 padding-top:0px!important;
}
.x-portlet .x-panel-ml {
 background-color: #DFE8F6;
 background-image:url(../images/portlet/left-right.gif)!important;
 padding-left:1px!important;
}
.x-portlet .x-panel-mr {
 background-image: url(../images/portlet/left-right.gif)!important;
 padding-right:4px!important;
}
.x-portlet .x-panel-nofooter .x-panel-bc, .x-panel-nofooter .x-window-bc {
 height:4px!important;
}
.x-portlet .x-panel-tl {
 border-bottom:0 none!important;
}
.x-portlet .x-panel-tl .x-panel-header {
 padding:6px 0 3px 0!important;
}
.x-panel-ghost .x-panel-tl .x-panel-header {
 padding:6px 0 2px 0!important;
}
/*portal收缩后样式*/
.x-panel-collapsed .x-panel-tc {
 background-image: url(../images/portlet/top-bottom2.gif)!important;
}
.x-panel-collapsed .x-panel-tl .x-panel-header {
 padding:6px 0 6px 0!important;
}
.x-panel-collapsed .x-panel-tl,.x-panel-collapsed .x-panel-tr, .x-panel-bl, .x-panel-br {
 background-image: url(../images/portlet/corners-sprite2.gif)!important;
}
/*
/*量图
*/
.x-progress-wrap {
    border-color:#6593cf;
	border:none;
}
.x-progress-wrap div{
	height:14px!important;
}
.x-progress-text {
    font-size:11px!important;
    font-weight:bold;
    color:#fff;
	padding:0px;
}
.x-progress-text-back {
    color:#396095;
	line-height:14px;
}
.x-progress-inner {
    background-color:#fff;
    border:solid 1px #41873A;
    padding:1px!important;
    background:repeat-x;
    position:relative;
}
.x-progress-inner-80 {
    border-color:#BF9500!important;
}
.x-progress-bar {
    background-color:#41873A!important;
	background-image:url(none)!important;
	border:none!important;
	font-size:1px!important;
}
.x-progress-bar-80 {
    background-color:#E9A503!important;
}
/*表格量表*/
.x-grid3-scroller .x-progress-inner {
    background-color:#fff;
    border:none!important;
    padding:1px!important;
    background:repeat-x;
    position:relative;
}
.x-grid3-scroller .x-progress-bar {
	float:right;
}

/*加载量图*/
.x-portlet .x-progress-inner,
.x-portlet .x-progress-bar,
.x-grid3-scroller .x-progress-inner,
.x-grid3-scroller .x-progress-bar,
.sf-accelerateatatus .x-progress-inner,
.sf-accelerateatatus .x-progress-bar,
.x-tip .x-progress-inner,
.x-tip .x-progress-bar{
    height:8px!important;
}
/*加速量图*/
.sf-accelerateatatus span{
	margin-right:15px;
}

/**/
.x-split-img-80 {
    width: 1px;
    height: 100%;
    border: 0 none;
    background-image: url(../images/x-80.gif);
}
/**/
.x-portlet .x-tool-close {
background-position:0 -360px;
}
.x-portlet .x-tool-close-over {
background-position:-15px -360px;
}
/* IE8下img有泄漏，换用div模拟 by zz, at 2010/07/14 */
div.sf-ico {
	display : inline-block;
}

.sf-ico, .x-cellicon img {
    width: 16px;
    height: 16px;
	vertical-align:middle;
}
.sf-ico{
	background-repeat:no-repeat;
}

.x-cellicon img {
    margin: 0 2px;
}

.hand {
    cursor: pointer;
}

/*CRY, checkbox和radio的模拟图片样式*/
/*checkbox */
.sf-ico-checknone {
    background-image: url(../images/default/tree/checknone.gif) !important;
}

.sf-ico-checkpart {
    background-image: url(../images/default/tree/checkpart.gif) !important;
}

.sf-ico-checkall {
    background-image: url(../images/default/tree/checkall.gif) !important;
}

.sf-ico-checknone-gray {
    background-image: url(../images/default/tree/checknone_gray.gif) !important;
}

.sf-ico-checkpart-gray {
    background-image: url(../images/default/tree/checkpart_gray.gif) !important;
}

.sf-ico-checkall-gray {
    background-image: url(../images/default/tree/checkall_gray.gif) !important;
}

.x-grid3-hd-chker {
    background-image: url(../images/default/grid/row-check-sprite.gif);
}

.x-grid3-hd-chker-on .x-grid3-hd-chker {
    background-position: -30px 0px;
}

.x-grid3-hd-chker-reverse .x-grid3-hd-chker {
    background-position: -60px 0px;
}

/*新增编辑删除*/
.sf-ico-add {
    background-image: url( ../images/ico/add.gif ) !important;
}
.sf-ico-multiadd{
	background-image: url( ../images/ico/multiadd.gif ) !important;
}
.sf-ico-edit, .x-cellicon-edit {
    background-image: url( ../images/ico/edit.gif ) !important;
}

.sf-ico-delete, .x-cellicon-delete {
    background-image: url( ../images/ico/delete.gif ) !important;
}

/*新增子通道*/
.sf-ico-add_subchannel {
    background-image: url( ../images/ico/add_subchannel.gif ) !important;
}

/*上移下移*/
.sf-ico-up, .x-cellicon-moveup {
    background-image: url( ../images/ico/top-move.gif ) !important;
}

.sf-ico-down, .x-cellicon-movedown {
    background-image: url( ../images/ico/under-move.gif ) !important;
}
/*上移下移灰色*/
.x-cellicon-moveup-disable {
    background-image: url( ../images/ico/top-move-disable.gif ) !important;
	cursor:default!important;
}

.x-cellicon-movedown-disable {
    background-image: url( ../images/ico/under-move-disable.gif ) !important;
	cursor:default!important;
}
/**/
.sf-ico-detail {
    background-image: url( ../images/ico/detail.gif) !important;
}

.sf-ico-config {
    background-image: url( ../images/ico/config.gif) !important;
}

/*页面中的灰色删除*/
.sf-ico-delete-disable {
    background-image: url( ../images/ico/delete_2.gif ) !important;
	cursor:default;
}

/*
 .sf-ico-delete-disable:hover, .x-cellicon-delete {
 background-image: url( ../images/ico/delete.gif ) !important;
 }
 */
/*允许拒绝*/
.sf-ico-accept {
    background-image: url( ../images/ico/accept.gif ) !important;
}

.sf-ico-refuse {
    background-image: url( ../images/ico/refuse.gif ) !important;
}

/*打勾、不打勾*/
.sf-ico-check, .x-cellicon-check {
    background-image: url( ../images/default/tree/checkall.gif ) !important;
}

.sf-ico-uncheck, .x-cellicon-uncheck {
    background-image: url( ../images/default/tree/checknone.gif ) !important;
}

/*启用禁用*/
.sf-ico-enable, .x-cellicon-enable {
    background-image: url( ../images/ico/enable.gif ) !important;
}

.sf-ico-disable, .x-cellicon-disable {
    background-image: url( ../images/ico/disable.gif ) !important;
}

.sf-ico-enable-gray {
    background-image: url( ../images/ico/enable02.gif ) !important;
	cursor:default;
}

.sf-ico-disable-gray {
    background-image: url( ../images/ico/disable02.gif ) !important;
	cursor:default;
}

/* 网口启用禁用 */
.sf-ico-port-active {
    background-image: url( ../images/eth_on.gif ) !important;
}

.sf-ico-port-inactive {
    background-image: url( ../images/eth_off.gif ) !important;
}

.sf-ico-port-inactive, .sf-ico-port-active {
    width: 24px !important;
    height: 19px !important;
}

/*导入导出*/
.sf-ico-import {
    background-image: url( ../images/ico/leading_in.gif ) !important;
}

.sf-ico-export {
    background-image: url( ../images/ico/leading_out.gif ) !important;
}

/*更新*/
.sf-ico-update {
    background-image: url( ../images/ico/updateBtn.gif ) !important;
}

/*添加模块、恢复默认*/
.sf-ico-add_portal {
    background-image: url( ../images/ico/add_portal.gif) !important;
}

.sf-ico-default_portal,.sf-ico-default {
    background-image: url( ../images/ico/default_portal.gif) !important;
}
/*停止刷新、刷新*/
.sf-ico-refresh-pause {
    background-image: url( ../images/ico/pause_refresh.gif) !important;
}

.sf-ico-refresh {
    background-image: url( ../images/ico/refresh.gif ) !important;
}

/*过滤条件*/
.sf-ico-filter {
    background-image: url( ../images/ico/filtering.gif) !important;
	width: 16px;
    height: 16px;
}

/*冻结、解冻*/
.sf-ico-frozen {
    background-image: url( ../images/ico/frozen.gif) !important;
	width: 16px;
    height: 16px;
}

.sf-ico-defrost {
    background-image: url( ../images/ico/defrost.gif ) !important;
}

/*查询*/
.sf-ico-search {
    background-image: url( ../images/ico/search.gif) !important;
}

/*选择全部*/
.sf-ico-select {
    background-image: url( ../images/ico/select.gif) !important;
}

/*移动子组及用户*/
.sf-ico-move {
    background-image: url( ../images/ico/move.gif) !important;
}

/*添加组,用户,多用户*/
.sf-ico-addtroop {
    background-image: url( ../images/ico/add_troop.gif) !important;
}

.sf-ico-adduser {
    background-image: url( ../images/ico/add_user.gif) !important;
}

.sf-ico-adduser-two {
    background-image: url( ../images/ico/add_user_two.gif) !important;
}

.sf-ico-user_two {
    background-image: url( ../images/ico/user_two.gif) !important;
}

/*组,用户*/
.troop {
    background-image: url( ../images/ico/troop.gif) !important;
}

.user {
    background-image: url( ../images/ico/user.gif) !important;
}

/*选择当前页、选择所有页*/
.sf-ico-current-page {
    background-image: url( ../images/ico/current_page.gif) !important;
}

.sf-ico-all-page {
    background-image: url( ../images/ico/all_page.gif) !important;
}

.sf-ico-tip {
    background-image: url( ../images/ico/tip.png) !important;
}

.sf-ico-auditpass {
    background-image: url( ../images/ico/auditpass.gif) !important;
}

.sf-ico-auditstop {
    background-image: url( ../images/ico/auditstop.gif) !important;
}

/*告警*/
.sf-ico-warn, .x-cellicon-info, .x-cellicon-error, .x-cellicon-alert {
    background-image: url( ../images/ico/warn.gif) !important;
}

/*生成策略报表*/
.sf-ico-tactics-report {
    background-image: url( ../images/ico/tactics_report.gif) !important;
}

/*储存使用偏好*/
.sf-ico-save-preferences {
    background-image: url( ../images/ico/save_preferences.gif) !important;
}

/*清除*/
.sf-ico-eliminate {
    background-image: url( ../images/ico/eliminate.gif) !important;
}

/*回滚*/
.sf-ico-rollback {
    background-image: url( ../images/ico/Rollback.gif) !important;
}

/*灰色回滚*/
.sf-ico-rollback-disable {
    background-image: url( ../images/ico/Rollback_disable.gif) !important;
	cursor:default;
}

/*网页学习*/
.sf-ico-weblearn {
    background-image: url( ../images/ico/web_learn.gif) !important;
}

/*URL更新*/
.sf-ico-url {
    background-image: url( ../images/ico/url.gif) !important;
}

/*统计*/
.sf-ico-statistics {
    background-image: url( ../images/ico/statistics.gif) !important;
}

/*设置*/
.sf-ico-config {
    background-image: url( ../images/ico/config.gif) !important;
}

/*向左*/
.sf-ico-toLeft {
    background-image: url( ../images/ico/left.gif) !important;
}

/*向右*/
.sf-ico-toRight {
    background-image: url( ../images/ico/right.gif) !important;
}

/*展开/收起*/
.sf-ico-expand {
    background-image: url( ../images/ico/expand-all.gif) !important;
}

.sf-ico-collapse {
    background-image: url( ../images/ico/collapse-all.gif) !important;
}

/*预览/恢复上次*/
.sf-ico-preview {
    background-image: url( ../images/ico/preview.gif) !important;
}

.sf-ico-Revert {
    background-image: url( ../images/ico/Revert.gif) !important;
}
.sf-ico-default {
    background-image: url( ../images/ico/default.gif) !important;
}


/*计算机*/
.sf-ico-computer {
    background-image: url( ../images/ico/computer.gif) !important;
}
/*柱图、饼图*/
.sf-ico-column{
	 background-image: url( ../images/ico/column.gif) !important;
}
.sf-ico-pie{
	 background-image: url( ../images/ico/pie.gif) !important;
}
/*流速、流量*/
.sf-ico-fluxRate{
	 background-image: url( ../images/ico/fluxRate.gif) !important;
}
.sf-ico-flux{
	 background-image: url( ../images/ico/flux.gif) !important;
}
/*消息*/
.sf-ico-news{
    background-image: url( ../images/ico/news.gif) !important;
}
/*有消息时*/
.sf-ico-news-yes{
    background-image: url( ../images/ico/news_yes.gif) !important;
}

/*返回*/
.sf-ico-return{
    background-image: url( ../images/ico/return.gif) !important;
}
/*新TAB页*/
.sf-ico-newtab{
    background-image: url( ../images/ico/new_tab.gif) !important;
}
/*新TAB页*/
.sf-conn-dc{
	background-image: url( ../images/ico/conn_dc.gif) !important;
}
/*仅允许登录POST（同告警图标一样）*/
.sf-ico-acceptpost{
	background-image: url( ../images/ico/warn.gif) !important;
}
/*立即同步*/
.sf-ico-synchronous{
	background-image: url( ../images/ico/synchronous.gif) !important;
}
/*立即生效配置*/
.sf-ico-immediate{
	background-image: url( ../images/ico/immediate.gif) !important;
}
/*记录并拒绝*/
.sf-ico-edit-disable{
	background-image: url( ../images/ico/edit_disable.gif) !important;
}
/*更新*/
.sf-ico-sync{
	background-image: url( ../images/ico/sync_dc.gif) !important;
}
/*角色*/
.sf-ico-role{
	background-image: url( ../images/ico/role.gif) !important;
}
/*页面帮助按钮*/
.sf-ico-help{
	background-image: url( ../images/ico/help.gif) !important;
}
/*开启*/
.sf-ico-open{
	background-image: url( ../images/ico/open.gif) !important;
}
/*关闭*/
.sf-ico-close{
	background-image: url( ../images/ico/close.gif) !important;
}
/* /style/main end */ 
