require.config({
	shim : {
		foundation : {
			deps : [ "jquery", "modernizr" ]
		},
		foundationTab : {
			deps : [ "foundation" ]
		}
	},
	paths : {
		jquery : 'libs/jquery/jquery-2.1.1.min',
		underscore : 'libs/underscore/underscore-min',
		backbone : 'libs/backbone/backbone-min',
		modernizr : 'libs/modernizr/modernizr',
		foundation : 'libs/foundation/foundation',
		foundationTab : 'libs/foundation/foundation.tab'
	}
});

require(
[ 
  'app',
  'jquery',
  'foundation',
  'foundationTab'
], 
function(App) {
	App.initialize();
	$(document).foundation();
	$(window).resize(function() {resizeElements();});
	$(document).ready(function() {resizeElements();});

	var event = new CustomEvent(
		"customSamlEditor", 
		{
			detail: {
				message: "Customized saml meta editor",
				time: new Date(),
			},
			bubbles: true,
			cancelable: true
		}
		);

	document.getElementById("samlmetaeditor").dispatchEvent(event);  
});


function resizeElements(){
	$("#xmlcontent").height(window.innerHeight - 524);
	$("#tree").height(window.innerHeight - 204);
}