// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('cljs_http.client');
goog.require('cljs.core');
goog.require('goog.Uri');
goog.require('cljs_http.core');
goog.require('cljs.core.async');
goog.require('no.en.core');
goog.require('cljs_http.util');
goog.require('clojure.string');
goog.require('cljs.reader');
cljs_http.client.if_pos = (function cljs_http$client$if_pos(v){
if(cljs.core.truth_((function (){var and__6141__auto__ = v;
if(cljs.core.truth_(and__6141__auto__)){
return (v > (0));
} else {
return and__6141__auto__;
}
})())){
return v;
} else {
return null;
}
});
/**
 * Parse `s` as query params and return a hash map.
 */
cljs_http.client.parse_query_params = (function cljs_http$client$parse_query_params(s){
if(!(clojure.string.blank_QMARK_(s))){
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3((function (p1__70795_SHARP_,p2__70794_SHARP_){
var vec__70797 = clojure.string.split.cljs$core$IFn$_invoke$arity$2(p2__70794_SHARP_,/=/);
var k = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70797,(0),null);
var v = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70797,(1),null);
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(p1__70795_SHARP_,cljs.core.keyword.cljs$core$IFn$_invoke$arity$1(no.en.core.url_decode(k)),no.en.core.url_decode(v));
}),cljs.core.PersistentArrayMap.EMPTY,clojure.string.split.cljs$core$IFn$_invoke$arity$2([cljs.core.str(s)].join(''),/&/));
} else {
return null;
}
});
/**
 * Parse `url` into a hash map.
 */
cljs_http.client.parse_url = (function cljs_http$client$parse_url(url){
if(!(clojure.string.blank_QMARK_(url))){
var uri = goog.Uri.parse(url);
var query_data = uri.getQueryData();
return new cljs.core.PersistentArrayMap(null, 6, [cljs.core.cst$kw$scheme,cljs.core.keyword.cljs$core$IFn$_invoke$arity$1(uri.getScheme()),cljs.core.cst$kw$server_DASH_name,uri.getDomain(),cljs.core.cst$kw$server_DASH_port,cljs_http.client.if_pos(uri.getPort()),cljs.core.cst$kw$uri,uri.getPath(),cljs.core.cst$kw$query_DASH_string,((cljs.core.not(query_data.isEmpty()))?[cljs.core.str(query_data)].join(''):null),cljs.core.cst$kw$query_DASH_params,((cljs.core.not(query_data.isEmpty()))?cljs_http.client.parse_query_params([cljs.core.str(query_data)].join('')):null)], null);
} else {
return null;
}
});
cljs_http.client.unexceptional_status_QMARK_ = new cljs.core.PersistentHashSet(null, new cljs.core.PersistentArrayMap(null, 13, [(205),null,(206),null,(300),null,(204),null,(307),null,(303),null,(301),null,(201),null,(302),null,(202),null,(200),null,(203),null,(207),null], null), null);
cljs_http.client.encode_val = (function cljs_http$client$encode_val(k,v){
return [cljs.core.str(no.en.core.url_encode(cljs.core.name(k))),cljs.core.str("="),cljs.core.str(no.en.core.url_encode([cljs.core.str(v)].join('')))].join('');
});
cljs_http.client.encode_vals = (function cljs_http$client$encode_vals(k,vs){
return clojure.string.join.cljs$core$IFn$_invoke$arity$2("&",cljs.core.map.cljs$core$IFn$_invoke$arity$2((function (p1__70798_SHARP_){
return cljs_http.client.encode_val(k,p1__70798_SHARP_);
}),vs));
});
cljs_http.client.encode_param = (function cljs_http$client$encode_param(p__70799){
var vec__70801 = p__70799;
var k = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70801,(0),null);
var v = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70801,(1),null);
if(cljs.core.coll_QMARK_(v)){
return cljs_http.client.encode_vals(k,v);
} else {
return cljs_http.client.encode_val(k,v);
}
});
cljs_http.client.generate_query_string = (function cljs_http$client$generate_query_string(params){
return clojure.string.join.cljs$core$IFn$_invoke$arity$2("&",cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs_http.client.encode_param,params));
});
cljs_http.client.regex_char_esc_smap = (function (){var esc_chars = "()*&^%$#!+";
return cljs.core.zipmap(esc_chars,cljs.core.map.cljs$core$IFn$_invoke$arity$2(((function (esc_chars){
return (function (p1__70802_SHARP_){
return [cljs.core.str("\\"),cljs.core.str(p1__70802_SHARP_)].join('');
});})(esc_chars))
,esc_chars));
})();
/**
 * Escape special characters -- for content-type.
 */
cljs_http.client.escape_special = (function cljs_http$client$escape_special(string){
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$2(cljs.core.str,cljs.core.replace.cljs$core$IFn$_invoke$arity$2(cljs_http.client.regex_char_esc_smap,string));
});
/**
 * Decocde the :body of `response` with `decode-fn` if the content type matches.
 */
cljs_http.client.decode_body = (function cljs_http$client$decode_body(response,decode_fn,content_type,request_method){
if(cljs.core.truth_((function (){var and__6141__auto__ = cljs.core.not_EQ_.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$head,request_method);
if(and__6141__auto__){
var and__6141__auto____$1 = cljs.core.not_EQ_.cljs$core$IFn$_invoke$arity$2((204),cljs.core.cst$kw$status.cljs$core$IFn$_invoke$arity$1(response));
if(and__6141__auto____$1){
return cljs.core.re_find(cljs.core.re_pattern([cljs.core.str("(?i)"),cljs.core.str(cljs_http.client.escape_special(content_type))].join('')),[cljs.core.str(cljs.core.get.cljs$core$IFn$_invoke$arity$3(cljs.core.cst$kw$headers.cljs$core$IFn$_invoke$arity$1(response),"content-type",""))].join(''));
} else {
return and__6141__auto____$1;
}
} else {
return and__6141__auto__;
}
})())){
return cljs.core.update_in.cljs$core$IFn$_invoke$arity$3(response,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$body], null),decode_fn);
} else {
return response;
}
});
/**
 * Encode :edn-params in the `request` :body and set the appropriate
 *   Content Type header.
 */
cljs_http.client.wrap_edn_params = (function cljs_http$client$wrap_edn_params(client){
return (function (request){
var temp__4655__auto__ = cljs.core.cst$kw$edn_DASH_params.cljs$core$IFn$_invoke$arity$1(request);
if(cljs.core.truth_(temp__4655__auto__)){
var params = temp__4655__auto__;
var headers = cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([new cljs.core.PersistentArrayMap(null, 1, ["content-type","application/edn"], null),cljs.core.cst$kw$headers.cljs$core$IFn$_invoke$arity$1(request)], 0));
var G__70804 = cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(request,cljs.core.cst$kw$edn_DASH_params),cljs.core.cst$kw$body,cljs.core.pr_str.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([params], 0))),cljs.core.cst$kw$headers,headers);
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(G__70804) : client.call(null,G__70804));
} else {
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(request) : client.call(null,request));
}
});
});
/**
 * Decode application/edn responses.
 */
cljs_http.client.wrap_edn_response = (function cljs_http$client$wrap_edn_response(client){
return (function (request){
return cljs.core.async.map.cljs$core$IFn$_invoke$arity$2((function (p1__70805_SHARP_){
return cljs_http.client.decode_body(p1__70805_SHARP_,cljs.reader.read_string,"application/edn",cljs.core.cst$kw$request_DASH_method.cljs$core$IFn$_invoke$arity$1(request));
}),new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(request) : client.call(null,request))], null));
});
});
cljs_http.client.wrap_default_headers = (function cljs_http$client$wrap_default_headers(var_args){
var args__7218__auto__ = [];
var len__7211__auto___70811 = arguments.length;
var i__7212__auto___70812 = (0);
while(true){
if((i__7212__auto___70812 < len__7211__auto___70811)){
args__7218__auto__.push((arguments[i__7212__auto___70812]));

var G__70813 = (i__7212__auto___70812 + (1));
i__7212__auto___70812 = G__70813;
continue;
} else {
}
break;
}

var argseq__7219__auto__ = ((((1) < args__7218__auto__.length))?(new cljs.core.IndexedSeq(args__7218__auto__.slice((1)),(0))):null);
return cljs_http.client.wrap_default_headers.cljs$core$IFn$_invoke$arity$variadic((arguments[(0)]),argseq__7219__auto__);
});

cljs_http.client.wrap_default_headers.cljs$core$IFn$_invoke$arity$variadic = (function (client,p__70808){
var vec__70809 = p__70808;
var default_headers = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70809,(0),null);
return ((function (vec__70809,default_headers){
return (function (request){
var temp__4655__auto__ = (function (){var or__6153__auto__ = cljs.core.cst$kw$default_DASH_headers.cljs$core$IFn$_invoke$arity$1(request);
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return default_headers;
}
})();
if(cljs.core.truth_(temp__4655__auto__)){
var default_headers__$1 = temp__4655__auto__;
var G__70810 = cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(request,cljs.core.cst$kw$default_DASH_headers,default_headers__$1);
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(G__70810) : client.call(null,G__70810));
} else {
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(request) : client.call(null,request));
}
});
;})(vec__70809,default_headers))
});

cljs_http.client.wrap_default_headers.cljs$lang$maxFixedArity = (1);

cljs_http.client.wrap_default_headers.cljs$lang$applyTo = (function (seq70806){
var G__70807 = cljs.core.first(seq70806);
var seq70806__$1 = cljs.core.next(seq70806);
return cljs_http.client.wrap_default_headers.cljs$core$IFn$_invoke$arity$variadic(G__70807,seq70806__$1);
});
cljs_http.client.wrap_accept = (function cljs_http$client$wrap_accept(var_args){
var args__7218__auto__ = [];
var len__7211__auto___70819 = arguments.length;
var i__7212__auto___70820 = (0);
while(true){
if((i__7212__auto___70820 < len__7211__auto___70819)){
args__7218__auto__.push((arguments[i__7212__auto___70820]));

var G__70821 = (i__7212__auto___70820 + (1));
i__7212__auto___70820 = G__70821;
continue;
} else {
}
break;
}

var argseq__7219__auto__ = ((((1) < args__7218__auto__.length))?(new cljs.core.IndexedSeq(args__7218__auto__.slice((1)),(0))):null);
return cljs_http.client.wrap_accept.cljs$core$IFn$_invoke$arity$variadic((arguments[(0)]),argseq__7219__auto__);
});

cljs_http.client.wrap_accept.cljs$core$IFn$_invoke$arity$variadic = (function (client,p__70816){
var vec__70817 = p__70816;
var accept = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70817,(0),null);
return ((function (vec__70817,accept){
return (function (request){
var temp__4655__auto__ = (function (){var or__6153__auto__ = cljs.core.cst$kw$accept.cljs$core$IFn$_invoke$arity$1(request);
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return accept;
}
})();
if(cljs.core.truth_(temp__4655__auto__)){
var accept__$1 = temp__4655__auto__;
var G__70818 = cljs.core.assoc_in(request,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$headers,"accept"], null),accept__$1);
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(G__70818) : client.call(null,G__70818));
} else {
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(request) : client.call(null,request));
}
});
;})(vec__70817,accept))
});

cljs_http.client.wrap_accept.cljs$lang$maxFixedArity = (1);

cljs_http.client.wrap_accept.cljs$lang$applyTo = (function (seq70814){
var G__70815 = cljs.core.first(seq70814);
var seq70814__$1 = cljs.core.next(seq70814);
return cljs_http.client.wrap_accept.cljs$core$IFn$_invoke$arity$variadic(G__70815,seq70814__$1);
});
cljs_http.client.wrap_content_type = (function cljs_http$client$wrap_content_type(var_args){
var args__7218__auto__ = [];
var len__7211__auto___70827 = arguments.length;
var i__7212__auto___70828 = (0);
while(true){
if((i__7212__auto___70828 < len__7211__auto___70827)){
args__7218__auto__.push((arguments[i__7212__auto___70828]));

var G__70829 = (i__7212__auto___70828 + (1));
i__7212__auto___70828 = G__70829;
continue;
} else {
}
break;
}

var argseq__7219__auto__ = ((((1) < args__7218__auto__.length))?(new cljs.core.IndexedSeq(args__7218__auto__.slice((1)),(0))):null);
return cljs_http.client.wrap_content_type.cljs$core$IFn$_invoke$arity$variadic((arguments[(0)]),argseq__7219__auto__);
});

cljs_http.client.wrap_content_type.cljs$core$IFn$_invoke$arity$variadic = (function (client,p__70824){
var vec__70825 = p__70824;
var content_type = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70825,(0),null);
return ((function (vec__70825,content_type){
return (function (request){
var temp__4655__auto__ = (function (){var or__6153__auto__ = cljs.core.cst$kw$content_DASH_type.cljs$core$IFn$_invoke$arity$1(request);
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return content_type;
}
})();
if(cljs.core.truth_(temp__4655__auto__)){
var content_type__$1 = temp__4655__auto__;
var G__70826 = cljs.core.assoc_in(request,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$headers,"content-type"], null),content_type__$1);
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(G__70826) : client.call(null,G__70826));
} else {
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(request) : client.call(null,request));
}
});
;})(vec__70825,content_type))
});

cljs_http.client.wrap_content_type.cljs$lang$maxFixedArity = (1);

cljs_http.client.wrap_content_type.cljs$lang$applyTo = (function (seq70822){
var G__70823 = cljs.core.first(seq70822);
var seq70822__$1 = cljs.core.next(seq70822);
return cljs_http.client.wrap_content_type.cljs$core$IFn$_invoke$arity$variadic(G__70823,seq70822__$1);
});
cljs_http.client.default_transit_opts = new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$encoding,cljs.core.cst$kw$json,cljs.core.cst$kw$encoding_DASH_opts,cljs.core.PersistentArrayMap.EMPTY,cljs.core.cst$kw$decoding,cljs.core.cst$kw$json,cljs.core.cst$kw$decoding_DASH_opts,cljs.core.PersistentArrayMap.EMPTY], null);
/**
 * Encode :transit-params in the `request` :body and set the appropriate
 *   Content Type header.
 * 
 *   A :transit-opts map can be optionally provided with the following keys:
 * 
 *   :encoding                #{:json, :json-verbose}
 *   :decoding                #{:json, :json-verbose}
 *   :encoding/decoding-opts  appropriate map of options to be passed to
 *                         transit writer/reader, respectively.
 */
cljs_http.client.wrap_transit_params = (function cljs_http$client$wrap_transit_params(client){
return (function (request){
var temp__4655__auto__ = cljs.core.cst$kw$transit_DASH_params.cljs$core$IFn$_invoke$arity$1(request);
if(cljs.core.truth_(temp__4655__auto__)){
var params = temp__4655__auto__;
var map__70833 = cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([cljs_http.client.default_transit_opts,cljs.core.cst$kw$transit_DASH_opts.cljs$core$IFn$_invoke$arity$1(request)], 0));
var map__70833__$1 = ((((!((map__70833 == null)))?((((map__70833.cljs$lang$protocol_mask$partition0$ & (64))) || (map__70833.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__70833):map__70833);
var encoding = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__70833__$1,cljs.core.cst$kw$encoding);
var encoding_opts = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__70833__$1,cljs.core.cst$kw$encoding_DASH_opts);
var headers = cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([new cljs.core.PersistentArrayMap(null, 1, ["content-type","application/transit+json"], null),cljs.core.cst$kw$headers.cljs$core$IFn$_invoke$arity$1(request)], 0));
var G__70835 = cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(request,cljs.core.cst$kw$transit_DASH_params),cljs.core.cst$kw$body,cljs_http.util.transit_encode(params,encoding,encoding_opts)),cljs.core.cst$kw$headers,headers);
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(G__70835) : client.call(null,G__70835));
} else {
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(request) : client.call(null,request));
}
});
});
/**
 * Decode application/transit+json responses.
 */
cljs_http.client.wrap_transit_response = (function cljs_http$client$wrap_transit_response(client){
return (function (request){
var map__70840 = cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([cljs_http.client.default_transit_opts,cljs.core.cst$kw$transit_DASH_opts.cljs$core$IFn$_invoke$arity$1(request)], 0));
var map__70840__$1 = ((((!((map__70840 == null)))?((((map__70840.cljs$lang$protocol_mask$partition0$ & (64))) || (map__70840.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__70840):map__70840);
var decoding = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__70840__$1,cljs.core.cst$kw$decoding);
var decoding_opts = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__70840__$1,cljs.core.cst$kw$decoding_DASH_opts);
var transit_decode = ((function (map__70840,map__70840__$1,decoding,decoding_opts){
return (function (p1__70836_SHARP_){
return cljs_http.util.transit_decode(p1__70836_SHARP_,decoding,decoding_opts);
});})(map__70840,map__70840__$1,decoding,decoding_opts))
;
return cljs.core.async.map.cljs$core$IFn$_invoke$arity$2(((function (map__70840,map__70840__$1,decoding,decoding_opts,transit_decode){
return (function (p1__70837_SHARP_){
return cljs_http.client.decode_body(p1__70837_SHARP_,transit_decode,"application/transit+json",cljs.core.cst$kw$request_DASH_method.cljs$core$IFn$_invoke$arity$1(request));
});})(map__70840,map__70840__$1,decoding,decoding_opts,transit_decode))
,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(request) : client.call(null,request))], null));
});
});
/**
 * Encode :json-params in the `request` :body and set the appropriate
 *   Content Type header.
 */
cljs_http.client.wrap_json_params = (function cljs_http$client$wrap_json_params(client){
return (function (request){
var temp__4655__auto__ = cljs.core.cst$kw$json_DASH_params.cljs$core$IFn$_invoke$arity$1(request);
if(cljs.core.truth_(temp__4655__auto__)){
var params = temp__4655__auto__;
var headers = cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([new cljs.core.PersistentArrayMap(null, 1, ["content-type","application/json"], null),cljs.core.cst$kw$headers.cljs$core$IFn$_invoke$arity$1(request)], 0));
var G__70843 = cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(request,cljs.core.cst$kw$json_DASH_params),cljs.core.cst$kw$body,cljs_http.util.json_encode(params)),cljs.core.cst$kw$headers,headers);
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(G__70843) : client.call(null,G__70843));
} else {
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(request) : client.call(null,request));
}
});
});
/**
 * Decode application/json responses.
 */
cljs_http.client.wrap_json_response = (function cljs_http$client$wrap_json_response(client){
return (function (request){
return cljs.core.async.map.cljs$core$IFn$_invoke$arity$2((function (p1__70844_SHARP_){
return cljs_http.client.decode_body(p1__70844_SHARP_,cljs_http.util.json_decode,"application/json",cljs.core.cst$kw$request_DASH_method.cljs$core$IFn$_invoke$arity$1(request));
}),new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(request) : client.call(null,request))], null));
});
});
cljs_http.client.wrap_query_params = (function cljs_http$client$wrap_query_params(client){
return (function (p__70849){
var map__70850 = p__70849;
var map__70850__$1 = ((((!((map__70850 == null)))?((((map__70850.cljs$lang$protocol_mask$partition0$ & (64))) || (map__70850.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__70850):map__70850);
var req = map__70850__$1;
var query_params = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__70850__$1,cljs.core.cst$kw$query_DASH_params);
if(cljs.core.truth_(query_params)){
var G__70852 = cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(req,cljs.core.cst$kw$query_DASH_params),cljs.core.cst$kw$query_DASH_string,cljs_http.client.generate_query_string(query_params));
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(G__70852) : client.call(null,G__70852));
} else {
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(req) : client.call(null,req));
}
});
});
cljs_http.client.wrap_form_params = (function cljs_http$client$wrap_form_params(client){
return (function (p__70857){
var map__70858 = p__70857;
var map__70858__$1 = ((((!((map__70858 == null)))?((((map__70858.cljs$lang$protocol_mask$partition0$ & (64))) || (map__70858.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__70858):map__70858);
var request = map__70858__$1;
var form_params = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__70858__$1,cljs.core.cst$kw$form_DASH_params);
var request_method = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__70858__$1,cljs.core.cst$kw$request_DASH_method);
var headers = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__70858__$1,cljs.core.cst$kw$headers);
if(cljs.core.truth_((function (){var and__6141__auto__ = form_params;
if(cljs.core.truth_(and__6141__auto__)){
return new cljs.core.PersistentHashSet(null, new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$patch,null,cljs.core.cst$kw$delete,null,cljs.core.cst$kw$post,null,cljs.core.cst$kw$put,null], null), null).call(null,request_method);
} else {
return and__6141__auto__;
}
})())){
var headers__$1 = cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([new cljs.core.PersistentArrayMap(null, 1, ["content-type","application/x-www-form-urlencoded"], null),headers], 0));
var G__70860 = cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(request,cljs.core.cst$kw$form_DASH_params),cljs.core.cst$kw$body,cljs_http.client.generate_query_string(form_params)),cljs.core.cst$kw$headers,headers__$1);
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(G__70860) : client.call(null,G__70860));
} else {
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(request) : client.call(null,request));
}
});
});
cljs_http.client.generate_form_data = (function cljs_http$client$generate_form_data(params){
var form_data = (new FormData());
var seq__70867_70873 = cljs.core.seq(params);
var chunk__70868_70874 = null;
var count__70869_70875 = (0);
var i__70870_70876 = (0);
while(true){
if((i__70870_70876 < count__70869_70875)){
var vec__70871_70877 = chunk__70868_70874.cljs$core$IIndexed$_nth$arity$2(null,i__70870_70876);
var k_70878 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70871_70877,(0),null);
var v_70879 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70871_70877,(1),null);
if(cljs.core.coll_QMARK_(v_70879)){
form_data.append(cljs.core.name(k_70878),cljs.core.first(v_70879),cljs.core.second(v_70879));
} else {
form_data.append(cljs.core.name(k_70878),v_70879);
}

var G__70880 = seq__70867_70873;
var G__70881 = chunk__70868_70874;
var G__70882 = count__70869_70875;
var G__70883 = (i__70870_70876 + (1));
seq__70867_70873 = G__70880;
chunk__70868_70874 = G__70881;
count__70869_70875 = G__70882;
i__70870_70876 = G__70883;
continue;
} else {
var temp__4657__auto___70884 = cljs.core.seq(seq__70867_70873);
if(temp__4657__auto___70884){
var seq__70867_70885__$1 = temp__4657__auto___70884;
if(cljs.core.chunked_seq_QMARK_(seq__70867_70885__$1)){
var c__6956__auto___70886 = cljs.core.chunk_first(seq__70867_70885__$1);
var G__70887 = cljs.core.chunk_rest(seq__70867_70885__$1);
var G__70888 = c__6956__auto___70886;
var G__70889 = cljs.core.count(c__6956__auto___70886);
var G__70890 = (0);
seq__70867_70873 = G__70887;
chunk__70868_70874 = G__70888;
count__70869_70875 = G__70889;
i__70870_70876 = G__70890;
continue;
} else {
var vec__70872_70891 = cljs.core.first(seq__70867_70885__$1);
var k_70892 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70872_70891,(0),null);
var v_70893 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70872_70891,(1),null);
if(cljs.core.coll_QMARK_(v_70893)){
form_data.append(cljs.core.name(k_70892),cljs.core.first(v_70893),cljs.core.second(v_70893));
} else {
form_data.append(cljs.core.name(k_70892),v_70893);
}

var G__70894 = cljs.core.next(seq__70867_70885__$1);
var G__70895 = null;
var G__70896 = (0);
var G__70897 = (0);
seq__70867_70873 = G__70894;
chunk__70868_70874 = G__70895;
count__70869_70875 = G__70896;
i__70870_70876 = G__70897;
continue;
}
} else {
}
}
break;
}

return form_data;
});
cljs_http.client.wrap_multipart_params = (function cljs_http$client$wrap_multipart_params(client){
return (function (p__70902){
var map__70903 = p__70902;
var map__70903__$1 = ((((!((map__70903 == null)))?((((map__70903.cljs$lang$protocol_mask$partition0$ & (64))) || (map__70903.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__70903):map__70903);
var request = map__70903__$1;
var multipart_params = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__70903__$1,cljs.core.cst$kw$multipart_DASH_params);
var request_method = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__70903__$1,cljs.core.cst$kw$request_DASH_method);
if(cljs.core.truth_((function (){var and__6141__auto__ = multipart_params;
if(cljs.core.truth_(and__6141__auto__)){
return new cljs.core.PersistentHashSet(null, new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$patch,null,cljs.core.cst$kw$delete,null,cljs.core.cst$kw$post,null,cljs.core.cst$kw$put,null], null), null).call(null,request_method);
} else {
return and__6141__auto__;
}
})())){
var G__70905 = cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(request,cljs.core.cst$kw$multipart_DASH_params),cljs.core.cst$kw$body,cljs_http.client.generate_form_data(multipart_params));
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(G__70905) : client.call(null,G__70905));
} else {
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(request) : client.call(null,request));
}
});
});
cljs_http.client.wrap_method = (function cljs_http$client$wrap_method(client){
return (function (req){
var temp__4655__auto__ = cljs.core.cst$kw$method.cljs$core$IFn$_invoke$arity$1(req);
if(cljs.core.truth_(temp__4655__auto__)){
var m = temp__4655__auto__;
var G__70907 = cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(req,cljs.core.cst$kw$method),cljs.core.cst$kw$request_DASH_method,m);
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(G__70907) : client.call(null,G__70907));
} else {
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(req) : client.call(null,req));
}
});
});
cljs_http.client.wrap_server_name = (function cljs_http$client$wrap_server_name(client,server_name){
return (function (p1__70908_SHARP_){
var G__70910 = cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(p1__70908_SHARP_,cljs.core.cst$kw$server_DASH_name,server_name);
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(G__70910) : client.call(null,G__70910));
});
});
cljs_http.client.wrap_url = (function cljs_http$client$wrap_url(client){
return (function (p__70916){
var map__70917 = p__70916;
var map__70917__$1 = ((((!((map__70917 == null)))?((((map__70917.cljs$lang$protocol_mask$partition0$ & (64))) || (map__70917.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__70917):map__70917);
var req = map__70917__$1;
var query_params = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__70917__$1,cljs.core.cst$kw$query_DASH_params);
var temp__4655__auto__ = cljs_http.client.parse_url(cljs.core.cst$kw$url.cljs$core$IFn$_invoke$arity$1(req));
if(cljs.core.truth_(temp__4655__auto__)){
var spec = temp__4655__auto__;
var G__70919 = cljs.core.update_in.cljs$core$IFn$_invoke$arity$3(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([req,spec], 0)),cljs.core.cst$kw$url),new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$query_DASH_params], null),((function (spec,temp__4655__auto__,map__70917,map__70917__$1,req,query_params){
return (function (p1__70911_SHARP_){
return cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([p1__70911_SHARP_,query_params], 0));
});})(spec,temp__4655__auto__,map__70917,map__70917__$1,req,query_params))
);
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(G__70919) : client.call(null,G__70919));
} else {
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(req) : client.call(null,req));
}
});
});
/**
 * Middleware converting the :basic-auth option or `credentials` into
 *   an Authorization header.
 */
cljs_http.client.wrap_basic_auth = (function cljs_http$client$wrap_basic_auth(var_args){
var args__7218__auto__ = [];
var len__7211__auto___70925 = arguments.length;
var i__7212__auto___70926 = (0);
while(true){
if((i__7212__auto___70926 < len__7211__auto___70925)){
args__7218__auto__.push((arguments[i__7212__auto___70926]));

var G__70927 = (i__7212__auto___70926 + (1));
i__7212__auto___70926 = G__70927;
continue;
} else {
}
break;
}

var argseq__7219__auto__ = ((((1) < args__7218__auto__.length))?(new cljs.core.IndexedSeq(args__7218__auto__.slice((1)),(0))):null);
return cljs_http.client.wrap_basic_auth.cljs$core$IFn$_invoke$arity$variadic((arguments[(0)]),argseq__7219__auto__);
});

cljs_http.client.wrap_basic_auth.cljs$core$IFn$_invoke$arity$variadic = (function (client,p__70922){
var vec__70923 = p__70922;
var credentials = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70923,(0),null);
return ((function (vec__70923,credentials){
return (function (req){
var credentials__$1 = (function (){var or__6153__auto__ = cljs.core.cst$kw$basic_DASH_auth.cljs$core$IFn$_invoke$arity$1(req);
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return credentials;
}
})();
if(!(cljs.core.empty_QMARK_(credentials__$1))){
var G__70924 = cljs.core.assoc_in(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(req,cljs.core.cst$kw$basic_DASH_auth),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$headers,"authorization"], null),cljs_http.util.basic_auth(credentials__$1));
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(G__70924) : client.call(null,G__70924));
} else {
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(req) : client.call(null,req));
}
});
;})(vec__70923,credentials))
});

cljs_http.client.wrap_basic_auth.cljs$lang$maxFixedArity = (1);

cljs_http.client.wrap_basic_auth.cljs$lang$applyTo = (function (seq70920){
var G__70921 = cljs.core.first(seq70920);
var seq70920__$1 = cljs.core.next(seq70920);
return cljs_http.client.wrap_basic_auth.cljs$core$IFn$_invoke$arity$variadic(G__70921,seq70920__$1);
});
/**
 * Middleware converting the :oauth-token option into an Authorization header.
 */
cljs_http.client.wrap_oauth = (function cljs_http$client$wrap_oauth(client){
return (function (req){
var temp__4655__auto__ = cljs.core.cst$kw$oauth_DASH_token.cljs$core$IFn$_invoke$arity$1(req);
if(cljs.core.truth_(temp__4655__auto__)){
var oauth_token = temp__4655__auto__;
var G__70929 = cljs.core.assoc_in(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(req,cljs.core.cst$kw$oauth_DASH_token),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$headers,"authorization"], null),[cljs.core.str("Bearer "),cljs.core.str(oauth_token)].join(''));
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(G__70929) : client.call(null,G__70929));
} else {
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(req) : client.call(null,req));
}
});
});
/**
 * Pipe the response-channel into the request-map's
 * custom channel (e.g. to enable transducers)
 */
cljs_http.client.wrap_channel_from_request_map = (function cljs_http$client$wrap_channel_from_request_map(client){
return (function (request){
var temp__4655__auto__ = cljs.core.cst$kw$channel.cljs$core$IFn$_invoke$arity$1(request);
if(cljs.core.truth_(temp__4655__auto__)){
var custom_channel = temp__4655__auto__;
return cljs.core.async.pipe.cljs$core$IFn$_invoke$arity$2((client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(request) : client.call(null,request)),custom_channel);
} else {
return (client.cljs$core$IFn$_invoke$arity$1 ? client.cljs$core$IFn$_invoke$arity$1(request) : client.call(null,request));
}
});
});
/**
 * Returns a batteries-included HTTP request function coresponding to the given
 * core client. See client/request
 */
cljs_http.client.wrap_request = (function cljs_http$client$wrap_request(request){
return cljs_http.client.wrap_default_headers(cljs_http.client.wrap_channel_from_request_map(cljs_http.client.wrap_url(cljs_http.client.wrap_method(cljs_http.client.wrap_oauth(cljs_http.client.wrap_basic_auth(cljs_http.client.wrap_query_params(cljs_http.client.wrap_content_type(cljs_http.client.wrap_json_response(cljs_http.client.wrap_json_params(cljs_http.client.wrap_transit_response(cljs_http.client.wrap_transit_params(cljs_http.client.wrap_edn_response(cljs_http.client.wrap_edn_params(cljs_http.client.wrap_multipart_params(cljs_http.client.wrap_form_params(cljs_http.client.wrap_accept(request)))))))))))))))));
});
/**
 * Executes the HTTP request corresponding to the given map and returns the
 * response map for corresponding to the resulting HTTP response.
 * 
 * In addition to the standard Ring request keys, the following keys are also
 * recognized:
 * * :url
 * * :method
 * * :query-params
 */
cljs_http.client.request = cljs_http.client.wrap_request(cljs_http.core.request);
/**
 * Like #'request, but sets the :method and :url as appropriate.
 */
cljs_http.client.delete$ = (function cljs_http$client$delete(var_args){
var args__7218__auto__ = [];
var len__7211__auto___70935 = arguments.length;
var i__7212__auto___70936 = (0);
while(true){
if((i__7212__auto___70936 < len__7211__auto___70935)){
args__7218__auto__.push((arguments[i__7212__auto___70936]));

var G__70937 = (i__7212__auto___70936 + (1));
i__7212__auto___70936 = G__70937;
continue;
} else {
}
break;
}

var argseq__7219__auto__ = ((((1) < args__7218__auto__.length))?(new cljs.core.IndexedSeq(args__7218__auto__.slice((1)),(0))):null);
return cljs_http.client.delete$.cljs$core$IFn$_invoke$arity$variadic((arguments[(0)]),argseq__7219__auto__);
});

cljs_http.client.delete$.cljs$core$IFn$_invoke$arity$variadic = (function (url,p__70932){
var vec__70933 = p__70932;
var req = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70933,(0),null);
var G__70934 = cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([req,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$method,cljs.core.cst$kw$delete,cljs.core.cst$kw$url,url], null)], 0));
return (cljs_http.client.request.cljs$core$IFn$_invoke$arity$1 ? cljs_http.client.request.cljs$core$IFn$_invoke$arity$1(G__70934) : cljs_http.client.request.call(null,G__70934));
});

cljs_http.client.delete$.cljs$lang$maxFixedArity = (1);

cljs_http.client.delete$.cljs$lang$applyTo = (function (seq70930){
var G__70931 = cljs.core.first(seq70930);
var seq70930__$1 = cljs.core.next(seq70930);
return cljs_http.client.delete$.cljs$core$IFn$_invoke$arity$variadic(G__70931,seq70930__$1);
});
/**
 * Like #'request, but sets the :method and :url as appropriate.
 */
cljs_http.client.get = (function cljs_http$client$get(var_args){
var args__7218__auto__ = [];
var len__7211__auto___70943 = arguments.length;
var i__7212__auto___70944 = (0);
while(true){
if((i__7212__auto___70944 < len__7211__auto___70943)){
args__7218__auto__.push((arguments[i__7212__auto___70944]));

var G__70945 = (i__7212__auto___70944 + (1));
i__7212__auto___70944 = G__70945;
continue;
} else {
}
break;
}

var argseq__7219__auto__ = ((((1) < args__7218__auto__.length))?(new cljs.core.IndexedSeq(args__7218__auto__.slice((1)),(0))):null);
return cljs_http.client.get.cljs$core$IFn$_invoke$arity$variadic((arguments[(0)]),argseq__7219__auto__);
});

cljs_http.client.get.cljs$core$IFn$_invoke$arity$variadic = (function (url,p__70940){
var vec__70941 = p__70940;
var req = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70941,(0),null);
var G__70942 = cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([req,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$method,cljs.core.cst$kw$get,cljs.core.cst$kw$url,url], null)], 0));
return (cljs_http.client.request.cljs$core$IFn$_invoke$arity$1 ? cljs_http.client.request.cljs$core$IFn$_invoke$arity$1(G__70942) : cljs_http.client.request.call(null,G__70942));
});

cljs_http.client.get.cljs$lang$maxFixedArity = (1);

cljs_http.client.get.cljs$lang$applyTo = (function (seq70938){
var G__70939 = cljs.core.first(seq70938);
var seq70938__$1 = cljs.core.next(seq70938);
return cljs_http.client.get.cljs$core$IFn$_invoke$arity$variadic(G__70939,seq70938__$1);
});
/**
 * Like #'request, but sets the :method and :url as appropriate.
 */
cljs_http.client.head = (function cljs_http$client$head(var_args){
var args__7218__auto__ = [];
var len__7211__auto___70951 = arguments.length;
var i__7212__auto___70952 = (0);
while(true){
if((i__7212__auto___70952 < len__7211__auto___70951)){
args__7218__auto__.push((arguments[i__7212__auto___70952]));

var G__70953 = (i__7212__auto___70952 + (1));
i__7212__auto___70952 = G__70953;
continue;
} else {
}
break;
}

var argseq__7219__auto__ = ((((1) < args__7218__auto__.length))?(new cljs.core.IndexedSeq(args__7218__auto__.slice((1)),(0))):null);
return cljs_http.client.head.cljs$core$IFn$_invoke$arity$variadic((arguments[(0)]),argseq__7219__auto__);
});

cljs_http.client.head.cljs$core$IFn$_invoke$arity$variadic = (function (url,p__70948){
var vec__70949 = p__70948;
var req = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70949,(0),null);
var G__70950 = cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([req,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$method,cljs.core.cst$kw$head,cljs.core.cst$kw$url,url], null)], 0));
return (cljs_http.client.request.cljs$core$IFn$_invoke$arity$1 ? cljs_http.client.request.cljs$core$IFn$_invoke$arity$1(G__70950) : cljs_http.client.request.call(null,G__70950));
});

cljs_http.client.head.cljs$lang$maxFixedArity = (1);

cljs_http.client.head.cljs$lang$applyTo = (function (seq70946){
var G__70947 = cljs.core.first(seq70946);
var seq70946__$1 = cljs.core.next(seq70946);
return cljs_http.client.head.cljs$core$IFn$_invoke$arity$variadic(G__70947,seq70946__$1);
});
/**
 * Like #'request, but sets the :method and :url as appropriate.
 */
cljs_http.client.jsonp = (function cljs_http$client$jsonp(var_args){
var args__7218__auto__ = [];
var len__7211__auto___70959 = arguments.length;
var i__7212__auto___70960 = (0);
while(true){
if((i__7212__auto___70960 < len__7211__auto___70959)){
args__7218__auto__.push((arguments[i__7212__auto___70960]));

var G__70961 = (i__7212__auto___70960 + (1));
i__7212__auto___70960 = G__70961;
continue;
} else {
}
break;
}

var argseq__7219__auto__ = ((((1) < args__7218__auto__.length))?(new cljs.core.IndexedSeq(args__7218__auto__.slice((1)),(0))):null);
return cljs_http.client.jsonp.cljs$core$IFn$_invoke$arity$variadic((arguments[(0)]),argseq__7219__auto__);
});

cljs_http.client.jsonp.cljs$core$IFn$_invoke$arity$variadic = (function (url,p__70956){
var vec__70957 = p__70956;
var req = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70957,(0),null);
var G__70958 = cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([req,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$method,cljs.core.cst$kw$jsonp,cljs.core.cst$kw$url,url], null)], 0));
return (cljs_http.client.request.cljs$core$IFn$_invoke$arity$1 ? cljs_http.client.request.cljs$core$IFn$_invoke$arity$1(G__70958) : cljs_http.client.request.call(null,G__70958));
});

cljs_http.client.jsonp.cljs$lang$maxFixedArity = (1);

cljs_http.client.jsonp.cljs$lang$applyTo = (function (seq70954){
var G__70955 = cljs.core.first(seq70954);
var seq70954__$1 = cljs.core.next(seq70954);
return cljs_http.client.jsonp.cljs$core$IFn$_invoke$arity$variadic(G__70955,seq70954__$1);
});
/**
 * Like #'request, but sets the :method and :url as appropriate.
 */
cljs_http.client.move = (function cljs_http$client$move(var_args){
var args__7218__auto__ = [];
var len__7211__auto___70967 = arguments.length;
var i__7212__auto___70968 = (0);
while(true){
if((i__7212__auto___70968 < len__7211__auto___70967)){
args__7218__auto__.push((arguments[i__7212__auto___70968]));

var G__70969 = (i__7212__auto___70968 + (1));
i__7212__auto___70968 = G__70969;
continue;
} else {
}
break;
}

var argseq__7219__auto__ = ((((1) < args__7218__auto__.length))?(new cljs.core.IndexedSeq(args__7218__auto__.slice((1)),(0))):null);
return cljs_http.client.move.cljs$core$IFn$_invoke$arity$variadic((arguments[(0)]),argseq__7219__auto__);
});

cljs_http.client.move.cljs$core$IFn$_invoke$arity$variadic = (function (url,p__70964){
var vec__70965 = p__70964;
var req = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70965,(0),null);
var G__70966 = cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([req,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$method,cljs.core.cst$kw$move,cljs.core.cst$kw$url,url], null)], 0));
return (cljs_http.client.request.cljs$core$IFn$_invoke$arity$1 ? cljs_http.client.request.cljs$core$IFn$_invoke$arity$1(G__70966) : cljs_http.client.request.call(null,G__70966));
});

cljs_http.client.move.cljs$lang$maxFixedArity = (1);

cljs_http.client.move.cljs$lang$applyTo = (function (seq70962){
var G__70963 = cljs.core.first(seq70962);
var seq70962__$1 = cljs.core.next(seq70962);
return cljs_http.client.move.cljs$core$IFn$_invoke$arity$variadic(G__70963,seq70962__$1);
});
/**
 * Like #'request, but sets the :method and :url as appropriate.
 */
cljs_http.client.options = (function cljs_http$client$options(var_args){
var args__7218__auto__ = [];
var len__7211__auto___70975 = arguments.length;
var i__7212__auto___70976 = (0);
while(true){
if((i__7212__auto___70976 < len__7211__auto___70975)){
args__7218__auto__.push((arguments[i__7212__auto___70976]));

var G__70977 = (i__7212__auto___70976 + (1));
i__7212__auto___70976 = G__70977;
continue;
} else {
}
break;
}

var argseq__7219__auto__ = ((((1) < args__7218__auto__.length))?(new cljs.core.IndexedSeq(args__7218__auto__.slice((1)),(0))):null);
return cljs_http.client.options.cljs$core$IFn$_invoke$arity$variadic((arguments[(0)]),argseq__7219__auto__);
});

cljs_http.client.options.cljs$core$IFn$_invoke$arity$variadic = (function (url,p__70972){
var vec__70973 = p__70972;
var req = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70973,(0),null);
var G__70974 = cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([req,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$method,cljs.core.cst$kw$options,cljs.core.cst$kw$url,url], null)], 0));
return (cljs_http.client.request.cljs$core$IFn$_invoke$arity$1 ? cljs_http.client.request.cljs$core$IFn$_invoke$arity$1(G__70974) : cljs_http.client.request.call(null,G__70974));
});

cljs_http.client.options.cljs$lang$maxFixedArity = (1);

cljs_http.client.options.cljs$lang$applyTo = (function (seq70970){
var G__70971 = cljs.core.first(seq70970);
var seq70970__$1 = cljs.core.next(seq70970);
return cljs_http.client.options.cljs$core$IFn$_invoke$arity$variadic(G__70971,seq70970__$1);
});
/**
 * Like #'request, but sets the :method and :url as appropriate.
 */
cljs_http.client.patch = (function cljs_http$client$patch(var_args){
var args__7218__auto__ = [];
var len__7211__auto___70983 = arguments.length;
var i__7212__auto___70984 = (0);
while(true){
if((i__7212__auto___70984 < len__7211__auto___70983)){
args__7218__auto__.push((arguments[i__7212__auto___70984]));

var G__70985 = (i__7212__auto___70984 + (1));
i__7212__auto___70984 = G__70985;
continue;
} else {
}
break;
}

var argseq__7219__auto__ = ((((1) < args__7218__auto__.length))?(new cljs.core.IndexedSeq(args__7218__auto__.slice((1)),(0))):null);
return cljs_http.client.patch.cljs$core$IFn$_invoke$arity$variadic((arguments[(0)]),argseq__7219__auto__);
});

cljs_http.client.patch.cljs$core$IFn$_invoke$arity$variadic = (function (url,p__70980){
var vec__70981 = p__70980;
var req = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70981,(0),null);
var G__70982 = cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([req,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$method,cljs.core.cst$kw$patch,cljs.core.cst$kw$url,url], null)], 0));
return (cljs_http.client.request.cljs$core$IFn$_invoke$arity$1 ? cljs_http.client.request.cljs$core$IFn$_invoke$arity$1(G__70982) : cljs_http.client.request.call(null,G__70982));
});

cljs_http.client.patch.cljs$lang$maxFixedArity = (1);

cljs_http.client.patch.cljs$lang$applyTo = (function (seq70978){
var G__70979 = cljs.core.first(seq70978);
var seq70978__$1 = cljs.core.next(seq70978);
return cljs_http.client.patch.cljs$core$IFn$_invoke$arity$variadic(G__70979,seq70978__$1);
});
/**
 * Like #'request, but sets the :method and :url as appropriate.
 */
cljs_http.client.post = (function cljs_http$client$post(var_args){
var args__7218__auto__ = [];
var len__7211__auto___70991 = arguments.length;
var i__7212__auto___70992 = (0);
while(true){
if((i__7212__auto___70992 < len__7211__auto___70991)){
args__7218__auto__.push((arguments[i__7212__auto___70992]));

var G__70993 = (i__7212__auto___70992 + (1));
i__7212__auto___70992 = G__70993;
continue;
} else {
}
break;
}

var argseq__7219__auto__ = ((((1) < args__7218__auto__.length))?(new cljs.core.IndexedSeq(args__7218__auto__.slice((1)),(0))):null);
return cljs_http.client.post.cljs$core$IFn$_invoke$arity$variadic((arguments[(0)]),argseq__7219__auto__);
});

cljs_http.client.post.cljs$core$IFn$_invoke$arity$variadic = (function (url,p__70988){
var vec__70989 = p__70988;
var req = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70989,(0),null);
var G__70990 = cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([req,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$method,cljs.core.cst$kw$post,cljs.core.cst$kw$url,url], null)], 0));
return (cljs_http.client.request.cljs$core$IFn$_invoke$arity$1 ? cljs_http.client.request.cljs$core$IFn$_invoke$arity$1(G__70990) : cljs_http.client.request.call(null,G__70990));
});

cljs_http.client.post.cljs$lang$maxFixedArity = (1);

cljs_http.client.post.cljs$lang$applyTo = (function (seq70986){
var G__70987 = cljs.core.first(seq70986);
var seq70986__$1 = cljs.core.next(seq70986);
return cljs_http.client.post.cljs$core$IFn$_invoke$arity$variadic(G__70987,seq70986__$1);
});
/**
 * Like #'request, but sets the :method and :url as appropriate.
 */
cljs_http.client.put = (function cljs_http$client$put(var_args){
var args__7218__auto__ = [];
var len__7211__auto___70999 = arguments.length;
var i__7212__auto___71000 = (0);
while(true){
if((i__7212__auto___71000 < len__7211__auto___70999)){
args__7218__auto__.push((arguments[i__7212__auto___71000]));

var G__71001 = (i__7212__auto___71000 + (1));
i__7212__auto___71000 = G__71001;
continue;
} else {
}
break;
}

var argseq__7219__auto__ = ((((1) < args__7218__auto__.length))?(new cljs.core.IndexedSeq(args__7218__auto__.slice((1)),(0))):null);
return cljs_http.client.put.cljs$core$IFn$_invoke$arity$variadic((arguments[(0)]),argseq__7219__auto__);
});

cljs_http.client.put.cljs$core$IFn$_invoke$arity$variadic = (function (url,p__70996){
var vec__70997 = p__70996;
var req = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70997,(0),null);
var G__70998 = cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([req,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$method,cljs.core.cst$kw$put,cljs.core.cst$kw$url,url], null)], 0));
return (cljs_http.client.request.cljs$core$IFn$_invoke$arity$1 ? cljs_http.client.request.cljs$core$IFn$_invoke$arity$1(G__70998) : cljs_http.client.request.call(null,G__70998));
});

cljs_http.client.put.cljs$lang$maxFixedArity = (1);

cljs_http.client.put.cljs$lang$applyTo = (function (seq70994){
var G__70995 = cljs.core.first(seq70994);
var seq70994__$1 = cljs.core.next(seq70994);
return cljs_http.client.put.cljs$core$IFn$_invoke$arity$variadic(G__70995,seq70994__$1);
});
