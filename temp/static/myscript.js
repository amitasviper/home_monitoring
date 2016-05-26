function setActive() {
	var tag_object = document.getElementById('cssmenu').getElementsByTagName('a');

  	var base_url = getBaseURL();					// -> http://localhost:3000
  	var base_url_length = base_url.length;			// -> 21
  	var absolute_page_url = window.location.href;	// -> http://localhost:3000/container/asd


  	var relative_page_url = absolute_page_url.substr(base_url_length+1, absolute_page_url.length);	// -> container/asd
  	var page_name = relative_page_url.substr(0, relative_page_url.indexOf('/'));			// -> container

  	//console.log("base_url: " + base_url + " absolute_page_url: " + absolute_page_url + " relative_page_url: " + relative_page_url + " page_name: " + page_name );

  	for( i=0; i<tag_object.length; i++) { 
  		var absolute_tag_url = tag_object[i].href;
  		var relative_tag_url = absolute_tag_url.substr(base_url_length+1, absolute_tag_url.length);
  		var tag_name = relative_tag_url.substr(0, relative_tag_url.indexOf('/'));
  		
  		//console.log("Comparing : " + tag_name + " Page Name : " + page_name);
    
    	if(tag_name==page_name) {
      		tag_object[i].parentElement.className='active';
    	}
    	else{
    		tag_object[i].parentElement.className='none';
    	}
  	}
}

function getBaseURL() {
        return location.protocol + "//" + location.hostname + (location.port && ":" + location.port);
}

$(function(){
    $('#side_nav').hover(function(){
        $(this).animate({width:'200px'},500);
        $('#page').animate({'margin-left':'200px'}, 500);
    },function(){
        $(this).animate({width:'35px'},500);
        $('#page').animate({'margin-left':'35px'}, 500);
    }).trigger('mouseleave');
});

window.onload = setActive();
