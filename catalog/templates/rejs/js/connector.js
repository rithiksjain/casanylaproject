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
  		 return $.getJSON(obj.url,function(results){
        console.log(results);
         // return results;
      });
  	}
  	else if (obj.method=="post"){
		return $.postJSON(obj.url,obj.data,function(results){
      console.log(results);
      // return results;
    });
  	}
  	else{
  		console.log("wrong method");
  	}

  }

  get_call(urls_in) {
  	var resp = {};
  	var deferred = Q.defer();
    // var deferred = $.Deferred()
    var urlCalls = [];
    urls = $.isArray(urls_in) ? urls_in : [{'url':urls_in, 'key':'default'}];
    var that=this;
    // console.log(urls);

  	$.each(urls, function(url) {
    	var obj={method: "get",
             url: urls[url].url,
             params: urls[url].params || {}
         };
         console.log(urls[url]);
         urlCalls.push(that.async_calls(obj));
       });

    $.when(...urlCalls)
      .then(
      function(...results) {
        var resp = {};
          $.each(urls, function(i,v){
            if (urls.length==1){
            resp[v.key] = results[i];
            }
            else{
            resp[v.key] = results[i][0];              
            }
          });
          deferred.resolve(resp)
      },
      function(...errors) {
          deferred.reject(errors);
          console.warn( errors.config.url, errors.status, errors.statusText );
      },
      function(...updates) {
          $.each(urls, function(i){
            if (urls.length==1){
              resp[urls[i].key] = updates[i].data;
            }else{
              resp[urls[i].key] = updates[i][0].data;
            }
          });
          deferred.update(resp);
    });

    return deferred.promise

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