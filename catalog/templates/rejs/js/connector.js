class async_helper {

  constructor() {
  }
/*
  log(obj){
  	console.log("i am just loggin");
  }*/

  async_calls(obj){
  	console.log("call starting");
  	if (obj.method=="get"){
  		return $.get(obj.url);
  	}
  	else if (obj.method=="post"){
		return $.post(obj.url,obj.data)
  	}
  	else{
  		console.log("wrong method");
  	}

  }

  get_call(urls_in) {
  	var resp = {};
  	var deferred = Q.defer();
    var urlCalls = [];
    urls = $.isArray(urls_in) ? urls_in : [{'url':urls_in, 'key':'default'}];
    var that=this;
  	$.each(urls, function(url) {
    	var obj={method: "get",
             url: urls[url].url,
             params: urls[url].params || {}
         };
         urlCalls.push(that.async_calls(obj));
         // console.log(urls[url]);
         // urlCalls.push(urls[url].url);
            });

    Q.all(urlCalls)
	    .then(
	    function(results) {
	        var resp = {};
	        $.each(urls, function(i){
	            resp[urls[i].key] = results[i].data;
	        });
	        /*deferred.resolve(
	            JSON.stringify(results))*/
	        deferred.resolve(resp)
	    },
	    function(errors) {
	        deferred.reject(errors);
	        console.warn( errors.config.url, errors.status, errors.statusText );
	    },
	    function(updates) {
	        $.each(urls, function(i){
	            resp[urls[i].key] = updates[i].data;
	        });
	        deferred.update(resp);
		});


    return deferred.promise;

  }

  post_call(url,data){
            var resp = {};
            var deferred = Q.defer();
            var request = this.async_calls(({
                method: "post",
                url: url,
                data: data
            }));
            request.then(
                function(results) {
                    /*deferred.resolve(
                        JSON.stringify(results)) */
                    resp = results.data;
                    deferred.resolve(resp);
                },
                function(errors) {
                    deferred.reject(errors);
                },
                function(updates) {
                    resp = updates.data;
                    deferred.update(resp);
            });

            return deferred.promise;
  }
}