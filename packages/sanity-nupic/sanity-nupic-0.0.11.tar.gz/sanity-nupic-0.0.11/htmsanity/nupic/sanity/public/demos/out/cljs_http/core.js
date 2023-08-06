// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('cljs_http.core');
goog.require('cljs.core');
goog.require('goog.net.ErrorCode');
goog.require('goog.net.EventType');
goog.require('cljs.core.async');
goog.require('cljs_http.util');
goog.require('goog.net.Jsonp');
goog.require('clojure.string');
goog.require('goog.net.XhrIo');
cljs_http.core.pending_requests = (function (){var G__68366 = cljs.core.PersistentArrayMap.EMPTY;
return (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(G__68366) : cljs.core.atom.call(null,G__68366));
})();
/**
 * Attempt to close the given channel and abort the pending HTTP request
 *   with which it is associated.
 */
cljs_http.core.abort_BANG_ = (function cljs_http$core$abort_BANG_(channel){
var temp__4657__auto__ = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(cljs_http.core.pending_requests) : cljs.core.deref.call(null,cljs_http.core.pending_requests)).call(null,channel);
if(cljs.core.truth_(temp__4657__auto__)){
var req = temp__4657__auto__;
cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$3(cljs_http.core.pending_requests,cljs.core.dissoc,channel);

cljs.core.async.close_BANG_(channel);

if(cljs.core.truth_(req.hasOwnProperty("abort"))){
return req.abort();
} else {
return cljs.core.cst$kw$jsonp.cljs$core$IFn$_invoke$arity$1(req).cancel(cljs.core.cst$kw$request.cljs$core$IFn$_invoke$arity$1(req));
}
} else {
return null;
}
});
cljs_http.core.aborted_QMARK_ = (function cljs_http$core$aborted_QMARK_(xhr){
return cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(xhr.getLastErrorCode(),goog.net.ErrorCode.ABORT);
});
/**
 * Takes an XhrIo object and applies the default-headers to it.
 */
cljs_http.core.apply_default_headers_BANG_ = (function cljs_http$core$apply_default_headers_BANG_(xhr,headers){
var formatted_h = cljs.core.zipmap(cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs_http.util.camelize,cljs.core.keys(headers)),cljs.core.vals(headers));
return cljs.core.dorun.cljs$core$IFn$_invoke$arity$1(cljs.core.map.cljs$core$IFn$_invoke$arity$2(((function (formatted_h){
return (function (p__68369){
var vec__68370 = p__68369;
var k = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__68370,(0),null);
var v = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__68370,(1),null);
return xhr.headers.set(k,v);
});})(formatted_h))
,formatted_h));
});
/**
 * Takes an XhrIo object and sets response-type if not nil.
 */
cljs_http.core.apply_response_type_BANG_ = (function cljs_http$core$apply_response_type_BANG_(xhr,response_type){
return xhr.setResponseType((function (){var G__68372 = response_type;
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$array_DASH_buffer,G__68372)){
return goog.net.XhrIo.ResponseType.ARRAY_BUFFER;
} else {
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$blob,G__68372)){
return goog.net.XhrIo.ResponseType.BLOB;
} else {
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$document,G__68372)){
return goog.net.XhrIo.ResponseType.DOCUMENT;
} else {
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$text,G__68372)){
return goog.net.XhrIo.ResponseType.TEXT;
} else {
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$default,G__68372)){
return goog.net.XhrIo.ResponseType.DEFAULT;
} else {
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(null,G__68372)){
return goog.net.XhrIo.ResponseType.DEFAULT;
} else {
throw (new Error([cljs.core.str("No matching clause: "),cljs.core.str(response_type)].join('')));

}
}
}
}
}
}
})());
});
/**
 * Builds an XhrIo object from the request parameters.
 */
cljs_http.core.build_xhr = (function cljs_http$core$build_xhr(p__68373){
var map__68377 = p__68373;
var map__68377__$1 = ((((!((map__68377 == null)))?((((map__68377.cljs$lang$protocol_mask$partition0$ & (64))) || (map__68377.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__68377):map__68377);
var request = map__68377__$1;
var with_credentials_QMARK_ = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__68377__$1,cljs.core.cst$kw$with_DASH_credentials_QMARK_);
var default_headers = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__68377__$1,cljs.core.cst$kw$default_DASH_headers);
var response_type = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__68377__$1,cljs.core.cst$kw$response_DASH_type);
var timeout = (function (){var or__6153__auto__ = cljs.core.cst$kw$timeout.cljs$core$IFn$_invoke$arity$1(request);
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return (0);
}
})();
var send_credentials = (((with_credentials_QMARK_ == null))?true:with_credentials_QMARK_);
var G__68379 = (new goog.net.XhrIo());
cljs_http.core.apply_default_headers_BANG_(G__68379,default_headers);

cljs_http.core.apply_response_type_BANG_(G__68379,response_type);

G__68379.setTimeoutInterval(timeout);

G__68379.setWithCredentials(send_credentials);

return G__68379;
});
cljs_http.core.error_kw = cljs.core.PersistentHashMap.fromArrays([(0),(7),(1),(4),(6),(3),(2),(9),(5),(8)],[cljs.core.cst$kw$no_DASH_error,cljs.core.cst$kw$abort,cljs.core.cst$kw$access_DASH_denied,cljs.core.cst$kw$custom_DASH_error,cljs.core.cst$kw$http_DASH_error,cljs.core.cst$kw$ff_DASH_silent_DASH_error,cljs.core.cst$kw$file_DASH_not_DASH_found,cljs.core.cst$kw$offline,cljs.core.cst$kw$exception,cljs.core.cst$kw$timeout]);
/**
 * Execute the HTTP request corresponding to the given Ring request
 *   map and return a core.async channel.
 */
cljs_http.core.xhr = (function cljs_http$core$xhr(p__68380){
var map__68408 = p__68380;
var map__68408__$1 = ((((!((map__68408 == null)))?((((map__68408.cljs$lang$protocol_mask$partition0$ & (64))) || (map__68408.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__68408):map__68408);
var request = map__68408__$1;
var request_method = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__68408__$1,cljs.core.cst$kw$request_DASH_method);
var headers = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__68408__$1,cljs.core.cst$kw$headers);
var body = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__68408__$1,cljs.core.cst$kw$body);
var with_credentials_QMARK_ = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__68408__$1,cljs.core.cst$kw$with_DASH_credentials_QMARK_);
var cancel = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__68408__$1,cljs.core.cst$kw$cancel);
var channel = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
var request_url = cljs_http.util.build_url(request);
var method = cljs.core.name((function (){var or__6153__auto__ = request_method;
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return cljs.core.cst$kw$get;
}
})());
var headers__$1 = cljs_http.util.build_headers(headers);
var xhr__$1 = cljs_http.core.build_xhr(request);
cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(cljs_http.core.pending_requests,cljs.core.assoc,channel,xhr__$1);

xhr__$1.listen(goog.net.EventType.COMPLETE,((function (channel,request_url,method,headers__$1,xhr__$1,map__68408,map__68408__$1,request,request_method,headers,body,with_credentials_QMARK_,cancel){
return (function (evt){
var target = evt.target;
var response = new cljs.core.PersistentArrayMap(null, 7, [cljs.core.cst$kw$status,target.getStatus(),cljs.core.cst$kw$success,target.isSuccess(),cljs.core.cst$kw$body,target.getResponse(),cljs.core.cst$kw$headers,cljs_http.util.parse_headers(target.getAllResponseHeaders()),cljs.core.cst$kw$trace_DASH_redirects,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [request_url,target.getLastUri()], null),cljs.core.cst$kw$error_DASH_code,(function (){var G__68410 = target.getLastErrorCode();
return (cljs_http.core.error_kw.cljs$core$IFn$_invoke$arity$1 ? cljs_http.core.error_kw.cljs$core$IFn$_invoke$arity$1(G__68410) : cljs_http.core.error_kw.call(null,G__68410));
})(),cljs.core.cst$kw$error_DASH_text,target.getLastError()], null);
if(cljs.core.not(cljs_http.core.aborted_QMARK_(xhr__$1))){
cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(channel,response);
} else {
}

cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$3(cljs_http.core.pending_requests,cljs.core.dissoc,channel);

if(cljs.core.truth_(cancel)){
cljs.core.async.close_BANG_(cancel);
} else {
}

return cljs.core.async.close_BANG_(channel);
});})(channel,request_url,method,headers__$1,xhr__$1,map__68408,map__68408__$1,request,request_method,headers,body,with_credentials_QMARK_,cancel))
);

xhr__$1.send(request_url,method,body,headers__$1);

if(cljs.core.truth_(cancel)){
var c__38109__auto___68435 = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto___68435,channel,request_url,method,headers__$1,xhr__$1,map__68408,map__68408__$1,request,request_method,headers,body,with_credentials_QMARK_,cancel){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto___68435,channel,request_url,method,headers__$1,xhr__$1,map__68408,map__68408__$1,request,request_method,headers,body,with_credentials_QMARK_,cancel){
return (function (state_68421){
var state_val_68422 = (state_68421[(1)]);
if((state_val_68422 === (1))){
var state_68421__$1 = state_68421;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_68421__$1,(2),cancel);
} else {
if((state_val_68422 === (2))){
var inst_68412 = (state_68421[(2)]);
var inst_68413 = xhr__$1.isComplete();
var inst_68414 = cljs.core.not(inst_68413);
var state_68421__$1 = (function (){var statearr_68423 = state_68421;
(statearr_68423[(7)] = inst_68412);

return statearr_68423;
})();
if(inst_68414){
var statearr_68424_68436 = state_68421__$1;
(statearr_68424_68436[(1)] = (3));

} else {
var statearr_68425_68437 = state_68421__$1;
(statearr_68425_68437[(1)] = (4));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_68422 === (3))){
var inst_68416 = xhr__$1.abort();
var state_68421__$1 = state_68421;
var statearr_68426_68438 = state_68421__$1;
(statearr_68426_68438[(2)] = inst_68416);

(statearr_68426_68438[(1)] = (5));


return cljs.core.cst$kw$recur;
} else {
if((state_val_68422 === (4))){
var state_68421__$1 = state_68421;
var statearr_68427_68439 = state_68421__$1;
(statearr_68427_68439[(2)] = null);

(statearr_68427_68439[(1)] = (5));


return cljs.core.cst$kw$recur;
} else {
if((state_val_68422 === (5))){
var inst_68419 = (state_68421[(2)]);
var state_68421__$1 = state_68421;
return cljs.core.async.impl.ioc_helpers.return_chan(state_68421__$1,inst_68419);
} else {
return null;
}
}
}
}
}
});})(c__38109__auto___68435,channel,request_url,method,headers__$1,xhr__$1,map__68408,map__68408__$1,request,request_method,headers,body,with_credentials_QMARK_,cancel))
;
return ((function (switch__37995__auto__,c__38109__auto___68435,channel,request_url,method,headers__$1,xhr__$1,map__68408,map__68408__$1,request,request_method,headers,body,with_credentials_QMARK_,cancel){
return (function() {
var cljs_http$core$xhr_$_state_machine__37996__auto__ = null;
var cljs_http$core$xhr_$_state_machine__37996__auto____0 = (function (){
var statearr_68431 = [null,null,null,null,null,null,null,null];
(statearr_68431[(0)] = cljs_http$core$xhr_$_state_machine__37996__auto__);

(statearr_68431[(1)] = (1));

return statearr_68431;
});
var cljs_http$core$xhr_$_state_machine__37996__auto____1 = (function (state_68421){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_68421);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e68432){if((e68432 instanceof Object)){
var ex__37999__auto__ = e68432;
var statearr_68433_68440 = state_68421;
(statearr_68433_68440[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_68421);

return cljs.core.cst$kw$recur;
} else {
throw e68432;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__68441 = state_68421;
state_68421 = G__68441;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
cljs_http$core$xhr_$_state_machine__37996__auto__ = function(state_68421){
switch(arguments.length){
case 0:
return cljs_http$core$xhr_$_state_machine__37996__auto____0.call(this);
case 1:
return cljs_http$core$xhr_$_state_machine__37996__auto____1.call(this,state_68421);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
cljs_http$core$xhr_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = cljs_http$core$xhr_$_state_machine__37996__auto____0;
cljs_http$core$xhr_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = cljs_http$core$xhr_$_state_machine__37996__auto____1;
return cljs_http$core$xhr_$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto___68435,channel,request_url,method,headers__$1,xhr__$1,map__68408,map__68408__$1,request,request_method,headers,body,with_credentials_QMARK_,cancel))
})();
var state__38111__auto__ = (function (){var statearr_68434 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_68434[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto___68435);

return statearr_68434;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto___68435,channel,request_url,method,headers__$1,xhr__$1,map__68408,map__68408__$1,request,request_method,headers,body,with_credentials_QMARK_,cancel))
);

} else {
}

return channel;
});
/**
 * Execute the JSONP request corresponding to the given Ring request
 *   map and return a core.async channel.
 */
cljs_http.core.jsonp = (function cljs_http$core$jsonp(p__68442){
var map__68459 = p__68442;
var map__68459__$1 = ((((!((map__68459 == null)))?((((map__68459.cljs$lang$protocol_mask$partition0$ & (64))) || (map__68459.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__68459):map__68459);
var request = map__68459__$1;
var timeout = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__68459__$1,cljs.core.cst$kw$timeout);
var callback_name = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__68459__$1,cljs.core.cst$kw$callback_DASH_name);
var cancel = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__68459__$1,cljs.core.cst$kw$cancel);
var channel = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
var jsonp__$1 = (new goog.net.Jsonp(cljs_http.util.build_url(request),callback_name));
jsonp__$1.setRequestTimeout(timeout);

var req_68475 = jsonp__$1.send(null,((function (channel,jsonp__$1,map__68459,map__68459__$1,request,timeout,callback_name,cancel){
return (function cljs_http$core$jsonp_$_success_callback(data){
var response = new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$status,(200),cljs.core.cst$kw$success,true,cljs.core.cst$kw$body,cljs.core.js__GT_clj.cljs$core$IFn$_invoke$arity$variadic(data,cljs.core.array_seq([cljs.core.cst$kw$keywordize_DASH_keys,true], 0))], null);
cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(channel,response);

cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$3(cljs_http.core.pending_requests,cljs.core.dissoc,channel);

if(cljs.core.truth_(cancel)){
cljs.core.async.close_BANG_(cancel);
} else {
}

return cljs.core.async.close_BANG_(channel);
});})(channel,jsonp__$1,map__68459,map__68459__$1,request,timeout,callback_name,cancel))
,((function (channel,jsonp__$1,map__68459,map__68459__$1,request,timeout,callback_name,cancel){
return (function cljs_http$core$jsonp_$_error_callback(){
cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$3(cljs_http.core.pending_requests,cljs.core.dissoc,channel);

if(cljs.core.truth_(cancel)){
cljs.core.async.close_BANG_(cancel);
} else {
}

return cljs.core.async.close_BANG_(channel);
});})(channel,jsonp__$1,map__68459,map__68459__$1,request,timeout,callback_name,cancel))
);
cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(cljs_http.core.pending_requests,cljs.core.assoc,channel,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$jsonp,jsonp__$1,cljs.core.cst$kw$request,req_68475], null));

if(cljs.core.truth_(cancel)){
var c__38109__auto___68476 = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto___68476,req_68475,channel,jsonp__$1,map__68459,map__68459__$1,request,timeout,callback_name,cancel){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto___68476,req_68475,channel,jsonp__$1,map__68459,map__68459__$1,request,timeout,callback_name,cancel){
return (function (state_68465){
var state_val_68466 = (state_68465[(1)]);
if((state_val_68466 === (1))){
var state_68465__$1 = state_68465;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_68465__$1,(2),cancel);
} else {
if((state_val_68466 === (2))){
var inst_68462 = (state_68465[(2)]);
var inst_68463 = jsonp__$1.cancel(req_68475);
var state_68465__$1 = (function (){var statearr_68467 = state_68465;
(statearr_68467[(7)] = inst_68462);

return statearr_68467;
})();
return cljs.core.async.impl.ioc_helpers.return_chan(state_68465__$1,inst_68463);
} else {
return null;
}
}
});})(c__38109__auto___68476,req_68475,channel,jsonp__$1,map__68459,map__68459__$1,request,timeout,callback_name,cancel))
;
return ((function (switch__37995__auto__,c__38109__auto___68476,req_68475,channel,jsonp__$1,map__68459,map__68459__$1,request,timeout,callback_name,cancel){
return (function() {
var cljs_http$core$jsonp_$_state_machine__37996__auto__ = null;
var cljs_http$core$jsonp_$_state_machine__37996__auto____0 = (function (){
var statearr_68471 = [null,null,null,null,null,null,null,null];
(statearr_68471[(0)] = cljs_http$core$jsonp_$_state_machine__37996__auto__);

(statearr_68471[(1)] = (1));

return statearr_68471;
});
var cljs_http$core$jsonp_$_state_machine__37996__auto____1 = (function (state_68465){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_68465);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e68472){if((e68472 instanceof Object)){
var ex__37999__auto__ = e68472;
var statearr_68473_68477 = state_68465;
(statearr_68473_68477[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_68465);

return cljs.core.cst$kw$recur;
} else {
throw e68472;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__68478 = state_68465;
state_68465 = G__68478;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
cljs_http$core$jsonp_$_state_machine__37996__auto__ = function(state_68465){
switch(arguments.length){
case 0:
return cljs_http$core$jsonp_$_state_machine__37996__auto____0.call(this);
case 1:
return cljs_http$core$jsonp_$_state_machine__37996__auto____1.call(this,state_68465);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
cljs_http$core$jsonp_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = cljs_http$core$jsonp_$_state_machine__37996__auto____0;
cljs_http$core$jsonp_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = cljs_http$core$jsonp_$_state_machine__37996__auto____1;
return cljs_http$core$jsonp_$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto___68476,req_68475,channel,jsonp__$1,map__68459,map__68459__$1,request,timeout,callback_name,cancel))
})();
var state__38111__auto__ = (function (){var statearr_68474 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_68474[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto___68476);

return statearr_68474;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto___68476,req_68475,channel,jsonp__$1,map__68459,map__68459__$1,request,timeout,callback_name,cancel))
);

} else {
}

return channel;
});
/**
 * Execute the HTTP request corresponding to the given Ring request
 *   map and return a core.async channel.
 */
cljs_http.core.request = (function cljs_http$core$request(p__68479){
var map__68482 = p__68479;
var map__68482__$1 = ((((!((map__68482 == null)))?((((map__68482.cljs$lang$protocol_mask$partition0$ & (64))) || (map__68482.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__68482):map__68482);
var request__$1 = map__68482__$1;
var request_method = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__68482__$1,cljs.core.cst$kw$request_DASH_method);
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(request_method,cljs.core.cst$kw$jsonp)){
return cljs_http.core.jsonp(request__$1);
} else {
return cljs_http.core.xhr(request__$1);
}
});
