// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.numenta.sanity.comportex.journal');
goog.require('cljs.core');
goog.require('clojure.set');
goog.require('org.nfrac.comportex.protocols');
goog.require('org.numenta.sanity.comportex.data');
goog.require('cljs.core.async');
goog.require('org.numenta.sanity.bridge.marshalling');
goog.require('org.numenta.sanity.comportex.details');
goog.require('org.nfrac.comportex.core');
goog.require('org.nfrac.comportex.util');
goog.require('clojure.walk');
org.numenta.sanity.comportex.journal.make_step = (function org$numenta$sanity$comportex$journal$make_step(htm,id){
var input_value = cljs.core.cst$kw$input_DASH_value.cljs$core$IFn$_invoke$arity$1(htm);
return new cljs.core.PersistentArrayMap(null, 4, ["snapshot-id",id,"timestep",org.nfrac.comportex.protocols.timestep(htm),"input-value",input_value,"sensed-values",cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,(function (){var iter__6925__auto__ = ((function (input_value){
return (function org$numenta$sanity$comportex$journal$make_step_$_iter__69570(s__69571){
return (new cljs.core.LazySeq(null,((function (input_value){
return (function (){
var s__69571__$1 = s__69571;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__69571__$1);
if(temp__4657__auto__){
var s__69571__$2 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(s__69571__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__69571__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__69573 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__69572 = (0);
while(true){
if((i__69572 < size__6924__auto__)){
var sense_id = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__69572);
var vec__69578 = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$sensors,sense_id], null));
var selector = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69578,(0),null);
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69578,(1),null);
var v = org.nfrac.comportex.protocols.extract(selector,input_value);
cljs.core.chunk_append(b__69573,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [sense_id,v], null));

var G__69580 = (i__69572 + (1));
i__69572 = G__69580;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__69573),org$numenta$sanity$comportex$journal$make_step_$_iter__69570(cljs.core.chunk_rest(s__69571__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__69573),null);
}
} else {
var sense_id = cljs.core.first(s__69571__$2);
var vec__69579 = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$sensors,sense_id], null));
var selector = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69579,(0),null);
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69579,(1),null);
var v = org.nfrac.comportex.protocols.extract(selector,input_value);
return cljs.core.cons(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [sense_id,v], null),org$numenta$sanity$comportex$journal$make_step_$_iter__69570(cljs.core.rest(s__69571__$2)));
}
} else {
return null;
}
break;
}
});})(input_value))
,null,null));
});})(input_value))
;
return iter__6925__auto__(org.nfrac.comportex.core.sense_keys(htm));
})())], null);
});
org.numenta.sanity.comportex.journal.id_missing_response = (function org$numenta$sanity$comportex$journal$id_missing_response(id,steps_offset){
var offset = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(steps_offset) : cljs.core.deref.call(null,steps_offset));
if((offset > (0))){
if((id < offset)){
} else {
throw (new Error([cljs.core.str("Assert failed: "),cljs.core.str(cljs.core.pr_str.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([cljs.core.list(cljs.core.cst$sym$_LT_,cljs.core.cst$sym$id,cljs.core.cst$sym$offset)], 0)))].join('')));
}

cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([[cljs.core.str("Can't fetch model "),cljs.core.str(id),cljs.core.str(". We've dropped all models below id "),cljs.core.str(offset)].join('')], 0));
} else {
}

return cljs.core.PersistentArrayMap.EMPTY;
});
org.numenta.sanity.comportex.journal.command_handler = (function org$numenta$sanity$comportex$journal$command_handler(current_model,steps_offset,model_steps,steps_mult,client_infos,capture_options){
var find_model = (function org$numenta$sanity$comportex$journal$command_handler_$_find_model(id){
if(typeof id === 'number'){
var i = (id - (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(steps_offset) : cljs.core.deref.call(null,steps_offset)));
if((i < (0))){
return null;
} else {
return cljs.core.nth.cljs$core$IFn$_invoke$arity$3((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(model_steps) : cljs.core.deref.call(null,model_steps)),i,null);
}
} else {
return null;
}
});
var find_model_pair = (function org$numenta$sanity$comportex$journal$command_handler_$_find_model_pair(id){
if(typeof id === 'number'){
var i = (id - (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(steps_offset) : cljs.core.deref.call(null,steps_offset)));
if((i > (0))){
var vec__69803 = cljs.core.subvec.cljs$core$IFn$_invoke$arity$3((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(model_steps) : cljs.core.deref.call(null,model_steps)),(i - (1)),(i + (1)));
var prev_step = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69803,(0),null);
var step = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69803,(1),null);
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2((org.nfrac.comportex.protocols.timestep(prev_step) + (1)),org.nfrac.comportex.protocols.timestep(step))){
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [prev_step,step], null);
} else {
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [null,step], null);
}
} else {
if((i === (0))){
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [null,cljs.core.nth.cljs$core$IFn$_invoke$arity$3((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(model_steps) : cljs.core.deref.call(null,model_steps)),i,null)], null);
} else {
return null;
}
}
} else {
return null;
}
});
return (function org$numenta$sanity$comportex$journal$command_handler_$_handle_command(p__69804){
var vec__69908 = p__69804;
var vec__69909 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69908,(0),null);
var command = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69909,(0),null);
var xs = cljs.core.nthnext(vec__69909,(1));
var client_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69908,(1),null);
var client_info = (function (){var or__6153__auto__ = cljs.core.get.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(client_infos) : cljs.core.deref.call(null,client_infos)),client_id);
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
var v = (function (){var G__69910 = cljs.core.PersistentArrayMap.EMPTY;
return (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(G__69910) : cljs.core.atom.call(null,G__69910));
})();
cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(client_infos,cljs.core.assoc,client_id,v);

return v;
}
})();
var G__69911 = command;
switch (G__69911) {
case "ping":
return null;

break;
case "client-disconnect":
cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["JOURNAL: Client disconnected."], 0));

return cljs.core.async.untap(steps_mult,cljs.core.cst$kw$ch.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$steps_DASH_mchannel.cljs$core$IFn$_invoke$arity$1((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(client_info) : cljs.core.deref.call(null,client_info)))));

break;
case "connect":
var vec__69912 = xs;
var old_client_info = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69912,(0),null);
var map__69913 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69912,(1),null);
var map__69913__$1 = ((((!((map__69913 == null)))?((((map__69913.cljs$lang$protocol_mask$partition0$ & (64))) || (map__69913.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__69913):map__69913);
var subscriber_c = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__69913__$1,cljs.core.cst$kw$ch);
cljs.core.add_watch(client_info,cljs.core.cst$kw$org$numenta$sanity$comportex$journal_SLASH_push_DASH_to_DASH_client,((function (vec__69912,old_client_info,map__69913,map__69913__$1,subscriber_c,G__69911,client_info,vec__69908,vec__69909,command,xs,client_id){
return (function (_,___$1,___$2,v){
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(subscriber_c,cljs.core.update.cljs$core$IFn$_invoke$arity$3(v,cljs.core.cst$kw$steps_DASH_mchannel,((function (vec__69912,old_client_info,map__69913,map__69913__$1,subscriber_c,G__69911,client_info,vec__69908,vec__69909,command,xs,client_id){
return (function (steps_mchannel){
return org.numenta.sanity.bridge.marshalling.channel_weak(cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(steps_mchannel,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$ch,cljs.core.cst$kw$target_DASH_id], null)));
});})(vec__69912,old_client_info,map__69913,map__69913__$1,subscriber_c,G__69911,client_info,vec__69908,vec__69909,command,xs,client_id))
));
});})(vec__69912,old_client_info,map__69913,map__69913__$1,subscriber_c,G__69911,client_info,vec__69908,vec__69909,command,xs,client_id))
);

var temp__4657__auto__ = old_client_info;
if(cljs.core.truth_(temp__4657__auto__)){
var map__69915 = temp__4657__auto__;
var map__69915__$1 = ((((!((map__69915 == null)))?((((map__69915.cljs$lang$protocol_mask$partition0$ & (64))) || (map__69915.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__69915):map__69915);
var steps_mchannel = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__69915__$1,cljs.core.cst$kw$steps_DASH_mchannel);
cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["JOURNAL: Client reconnected."], 0));

if(cljs.core.truth_(steps_mchannel)){
cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["JOURNAL: Client resubscribed to steps."], 0));

cljs.core.async.tap.cljs$core$IFn$_invoke$arity$2(steps_mult,cljs.core.cst$kw$ch.cljs$core$IFn$_invoke$arity$1(steps_mchannel));
} else {
}

return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$2(client_info,((function (map__69915,map__69915__$1,steps_mchannel,temp__4657__auto__,vec__69912,old_client_info,map__69913,map__69913__$1,subscriber_c,G__69911,client_info,vec__69908,vec__69909,command,xs,client_id){
return (function (p1__69581_SHARP_){
var G__69917 = p1__69581_SHARP_;
if(cljs.core.truth_(steps_mchannel)){
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(G__69917,cljs.core.cst$kw$steps_DASH_mchannel,steps_mchannel);
} else {
return G__69917;
}
});})(map__69915,map__69915__$1,steps_mchannel,temp__4657__auto__,vec__69912,old_client_info,map__69913,map__69913__$1,subscriber_c,G__69911,client_info,vec__69908,vec__69909,command,xs,client_id))
);
} else {
return null;
}

break;
case "consider-future":
var vec__69918 = xs;
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69918,(0),null);
var input = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69918,(1),null);
var map__69919 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69918,(2),null);
var map__69919__$1 = ((((!((map__69919 == null)))?((((map__69919.cljs$lang$protocol_mask$partition0$ & (64))) || (map__69919.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__69919):map__69919);
var response_c = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__69919__$1,cljs.core.cst$kw$ch);
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(response_c,(function (){var temp__4655__auto__ = find_model(id);
if(cljs.core.truth_(temp__4655__auto__)){
var htm = temp__4655__auto__;
return cljs.core.zipmap(org.nfrac.comportex.core.region_keys.cljs$core$IFn$_invoke$arity$1(htm),cljs.core.map.cljs$core$IFn$_invoke$arity$2(org.nfrac.comportex.core.column_state_freqs,org.nfrac.comportex.core.region_seq(org.nfrac.comportex.protocols.htm_activate(org.nfrac.comportex.protocols.htm_sense(htm,input,null)))));
} else {
return org.numenta.sanity.comportex.journal.id_missing_response(id,steps_offset);
}
})());

break;
case "decode-predictive-columns":
var vec__69921 = xs;
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69921,(0),null);
var sense_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69921,(1),null);
var n = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69921,(2),null);
var map__69922 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69921,(3),null);
var map__69922__$1 = ((((!((map__69922 == null)))?((((map__69922.cljs$lang$protocol_mask$partition0$ & (64))) || (map__69922.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__69922):map__69922);
var response_c = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__69922__$1,cljs.core.cst$kw$ch);
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(response_c,(function (){var temp__4655__auto__ = find_model(id);
if(cljs.core.truth_(temp__4655__auto__)){
var htm = temp__4655__auto__;
return org.nfrac.comportex.core.predictions.cljs$core$IFn$_invoke$arity$3(htm,sense_id,n);
} else {
return org.numenta.sanity.comportex.journal.id_missing_response(id,steps_offset);
}
})());

break;
case "get-steps":
var vec__69924 = xs;
var map__69925 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69924,(0),null);
var map__69925__$1 = ((((!((map__69925 == null)))?((((map__69925.cljs$lang$protocol_mask$partition0$ & (64))) || (map__69925.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__69925):map__69925);
var response_c = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__69925__$1,cljs.core.cst$kw$ch);
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(response_c,cljs.core.vec(cljs.core.map.cljs$core$IFn$_invoke$arity$3(org.numenta.sanity.comportex.journal.make_step,(cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(model_steps) : cljs.core.deref.call(null,model_steps)),cljs.core.drop.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(steps_offset) : cljs.core.deref.call(null,steps_offset)),cljs.core.range.cljs$core$IFn$_invoke$arity$0()))));

break;
case "subscribe":
var vec__69927 = xs;
var steps_mchannel = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69927,(0),null);
cljs.core.async.tap.cljs$core$IFn$_invoke$arity$2(steps_mult,cljs.core.cst$kw$ch.cljs$core$IFn$_invoke$arity$1(steps_mchannel));

cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(client_info,cljs.core.assoc,cljs.core.cst$kw$steps_DASH_mchannel,steps_mchannel);

return cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["JOURNAL: Client subscribed to steps."], 0));

break;
case "get-network-shape":
var vec__69928 = xs;
var map__69929 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69928,(0),null);
var map__69929__$1 = ((((!((map__69929 == null)))?((((map__69929.cljs$lang$protocol_mask$partition0$ & (64))) || (map__69929.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__69929):map__69929);
var response_c = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__69929__$1,cljs.core.cst$kw$ch);
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(response_c,org.numenta.sanity.comportex.data.network_shape((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(current_model) : cljs.core.deref.call(null,current_model))));

break;
case "get-capture-options":
var vec__69931 = xs;
var map__69932 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69931,(0),null);
var map__69932__$1 = ((((!((map__69932 == null)))?((((map__69932.cljs$lang$protocol_mask$partition0$ & (64))) || (map__69932.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__69932):map__69932);
var response_c = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__69932__$1,cljs.core.cst$kw$ch);
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(response_c,clojure.walk.stringify_keys((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(capture_options) : cljs.core.deref.call(null,capture_options))));

break;
case "set-capture-options":
var vec__69934 = xs;
var co = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69934,(0),null);
var G__69935 = capture_options;
var G__69936 = clojure.walk.keywordize_keys(co);
return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__69935,G__69936) : cljs.core.reset_BANG_.call(null,G__69935,G__69936));

break;
case "get-layer-bits":
var vec__69937 = xs;
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69937,(0),null);
var rgn_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69937,(1),null);
var lyr_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69937,(2),null);
var fetches = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69937,(3),null);
var map__69938 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69937,(4),null);
var map__69938__$1 = ((((!((map__69938 == null)))?((((map__69938.cljs$lang$protocol_mask$partition0$ & (64))) || (map__69938.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__69938):map__69938);
var cols_subset = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__69938__$1,cljs.core.cst$kw$value);
var map__69939 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69937,(5),null);
var map__69939__$1 = ((((!((map__69939 == null)))?((((map__69939.cljs$lang$protocol_mask$partition0$ & (64))) || (map__69939.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__69939):map__69939);
var response_c = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__69939__$1,cljs.core.cst$kw$ch);
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(response_c,(function (){var temp__4655__auto__ = find_model(id);
if(cljs.core.truth_(temp__4655__auto__)){
var htm = temp__4655__auto__;
var lyr = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,rgn_id,lyr_id], null));
var G__69942 = cljs.core.PersistentArrayMap.EMPTY;
var G__69942__$1 = ((cljs.core.contains_QMARK_(fetches,"active-columns"))?cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(G__69942,"active-columns",org.nfrac.comportex.protocols.active_columns(lyr)):G__69942);
var G__69942__$2 = ((cljs.core.contains_QMARK_(fetches,"pred-columns"))?cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(G__69942__$1,"pred-columns",cljs.core.distinct.cljs$core$IFn$_invoke$arity$1(cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs.core.first,org.nfrac.comportex.protocols.prior_predictive_cells(lyr)))):G__69942__$1);
var G__69942__$3 = ((cljs.core.contains_QMARK_(fetches,"overlaps-columns-alpha"))?cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(G__69942__$2,"overlaps-columns-alpha",org.nfrac.comportex.util.remap(((function (G__69942,G__69942__$1,G__69942__$2,lyr,htm,temp__4655__auto__,vec__69937,id,rgn_id,lyr_id,fetches,map__69938,map__69938__$1,cols_subset,map__69939,map__69939__$1,response_c,G__69911,client_info,vec__69908,vec__69909,command,xs,client_id){
return (function (p1__69582_SHARP_){
var x__6491__auto__ = 1.0;
var y__6492__auto__ = (p1__69582_SHARP_ / (16));
return ((x__6491__auto__ < y__6492__auto__) ? x__6491__auto__ : y__6492__auto__);
});})(G__69942,G__69942__$1,G__69942__$2,lyr,htm,temp__4655__auto__,vec__69937,id,rgn_id,lyr_id,fetches,map__69938,map__69938__$1,cols_subset,map__69939,map__69939__$1,response_c,G__69911,client_info,vec__69908,vec__69909,command,xs,client_id))
,cljs.core.persistent_BANG_(cljs.core.reduce_kv(((function (G__69942,G__69942__$1,G__69942__$2,lyr,htm,temp__4655__auto__,vec__69937,id,rgn_id,lyr_id,fetches,map__69938,map__69938__$1,cols_subset,map__69939,map__69939__$1,response_c,G__69911,client_info,vec__69908,vec__69909,command,xs,client_id){
return (function (m,p__69943,v){
var vec__69944 = p__69943;
var col = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69944,(0),null);
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69944,(1),null);
var ___$1 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69944,(2),null);
return cljs.core.assoc_BANG_.cljs$core$IFn$_invoke$arity$3(m,col,(function (){var x__6484__auto__ = v;
var y__6485__auto__ = cljs.core.get.cljs$core$IFn$_invoke$arity$3(m,col,(0));
return ((x__6484__auto__ > y__6485__auto__) ? x__6484__auto__ : y__6485__auto__);
})());
});})(G__69942,G__69942__$1,G__69942__$2,lyr,htm,temp__4655__auto__,vec__69937,id,rgn_id,lyr_id,fetches,map__69938,map__69938__$1,cols_subset,map__69939,map__69939__$1,response_c,G__69911,client_info,vec__69908,vec__69909,command,xs,client_id))
,cljs.core.transient$(cljs.core.PersistentArrayMap.EMPTY),cljs.core.cst$kw$col_DASH_overlaps.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$state.cljs$core$IFn$_invoke$arity$1(lyr)))))):G__69942__$2);
var G__69942__$4 = ((cljs.core.contains_QMARK_(fetches,"boost-columns-alpha"))?cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(G__69942__$3,"boost-columns-alpha",(function (){var map__69945 = org.nfrac.comportex.protocols.params(lyr);
var map__69945__$1 = ((((!((map__69945 == null)))?((((map__69945.cljs$lang$protocol_mask$partition0$ & (64))) || (map__69945.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__69945):map__69945);
var max_boost = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__69945__$1,cljs.core.cst$kw$max_DASH_boost);
return cljs.core.zipmap(cljs.core.range.cljs$core$IFn$_invoke$arity$0(),cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs.core.float$,cljs.core.map.cljs$core$IFn$_invoke$arity$2(((function (map__69945,map__69945__$1,max_boost,G__69942,G__69942__$1,G__69942__$2,G__69942__$3,lyr,htm,temp__4655__auto__,vec__69937,id,rgn_id,lyr_id,fetches,map__69938,map__69938__$1,cols_subset,map__69939,map__69939__$1,response_c,G__69911,client_info,vec__69908,vec__69909,command,xs,client_id){
return (function (p1__69583_SHARP_){
return ((p1__69583_SHARP_ - (1)) / (max_boost - (1)));
});})(map__69945,map__69945__$1,max_boost,G__69942,G__69942__$1,G__69942__$2,G__69942__$3,lyr,htm,temp__4655__auto__,vec__69937,id,rgn_id,lyr_id,fetches,map__69938,map__69938__$1,cols_subset,map__69939,map__69939__$1,response_c,G__69911,client_info,vec__69908,vec__69909,command,xs,client_id))
,cljs.core.cst$kw$boosts.cljs$core$IFn$_invoke$arity$1(lyr))));
})()):G__69942__$3);
var G__69942__$5 = ((cljs.core.contains_QMARK_(fetches,"active-freq-columns-alpha"))?cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(G__69942__$4,"active-freq-columns-alpha",cljs.core.zipmap(cljs.core.range.cljs$core$IFn$_invoke$arity$0(),cljs.core.map.cljs$core$IFn$_invoke$arity$2(((function (G__69942,G__69942__$1,G__69942__$2,G__69942__$3,G__69942__$4,lyr,htm,temp__4655__auto__,vec__69937,id,rgn_id,lyr_id,fetches,map__69938,map__69938__$1,cols_subset,map__69939,map__69939__$1,response_c,G__69911,client_info,vec__69908,vec__69909,command,xs,client_id){
return (function (p1__69584_SHARP_){
var x__6491__auto__ = 1.0;
var y__6492__auto__ = ((2) * p1__69584_SHARP_);
return ((x__6491__auto__ < y__6492__auto__) ? x__6491__auto__ : y__6492__auto__);
});})(G__69942,G__69942__$1,G__69942__$2,G__69942__$3,G__69942__$4,lyr,htm,temp__4655__auto__,vec__69937,id,rgn_id,lyr_id,fetches,map__69938,map__69938__$1,cols_subset,map__69939,map__69939__$1,response_c,G__69911,client_info,vec__69908,vec__69909,command,xs,client_id))
,cljs.core.cst$kw$active_DASH_duty_DASH_cycles.cljs$core$IFn$_invoke$arity$1(lyr)))):G__69942__$4);
var G__69942__$6 = ((cljs.core.contains_QMARK_(fetches,"n-segments-columns-alpha"))?cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(G__69942__$5,"n-segments-columns-alpha",cljs.core.zipmap(cols_subset,cljs.core.map.cljs$core$IFn$_invoke$arity$2(((function (G__69942,G__69942__$1,G__69942__$2,G__69942__$3,G__69942__$4,G__69942__$5,lyr,htm,temp__4655__auto__,vec__69937,id,rgn_id,lyr_id,fetches,map__69938,map__69938__$1,cols_subset,map__69939,map__69939__$1,response_c,G__69911,client_info,vec__69908,vec__69909,command,xs,client_id){
return (function (p1__69586_SHARP_){
var x__6491__auto__ = 1.0;
var y__6492__auto__ = (p1__69586_SHARP_ / 16.0);
return ((x__6491__auto__ < y__6492__auto__) ? x__6491__auto__ : y__6492__auto__);
});})(G__69942,G__69942__$1,G__69942__$2,G__69942__$3,G__69942__$4,G__69942__$5,lyr,htm,temp__4655__auto__,vec__69937,id,rgn_id,lyr_id,fetches,map__69938,map__69938__$1,cols_subset,map__69939,map__69939__$1,response_c,G__69911,client_info,vec__69908,vec__69909,command,xs,client_id))
,cljs.core.map.cljs$core$IFn$_invoke$arity$2(((function (G__69942,G__69942__$1,G__69942__$2,G__69942__$3,G__69942__$4,G__69942__$5,lyr,htm,temp__4655__auto__,vec__69937,id,rgn_id,lyr_id,fetches,map__69938,map__69938__$1,cols_subset,map__69939,map__69939__$1,response_c,G__69911,client_info,vec__69908,vec__69909,command,xs,client_id){
return (function (p1__69585_SHARP_){
return org.numenta.sanity.comportex.data.count_segs_in_column(cljs.core.cst$kw$distal_DASH_sg.cljs$core$IFn$_invoke$arity$1(lyr),org.nfrac.comportex.protocols.layer_depth(lyr),p1__69585_SHARP_);
});})(G__69942,G__69942__$1,G__69942__$2,G__69942__$3,G__69942__$4,G__69942__$5,lyr,htm,temp__4655__auto__,vec__69937,id,rgn_id,lyr_id,fetches,map__69938,map__69938__$1,cols_subset,map__69939,map__69939__$1,response_c,G__69911,client_info,vec__69908,vec__69909,command,xs,client_id))
,cols_subset)))):G__69942__$5);
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(G__69942__$6,"break?",cljs.core.empty_QMARK_(cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(lyr,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$prior_DASH_distal_DASH_state,cljs.core.cst$kw$active_DASH_bits], null))));

} else {
return org.numenta.sanity.comportex.journal.id_missing_response(id,steps_offset);
}
})());

break;
case "get-sense-bits":
var vec__69947 = xs;
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69947,(0),null);
var sense_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69947,(1),null);
var fetches = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69947,(2),null);
var map__69948 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69947,(3),null);
var map__69948__$1 = ((((!((map__69948 == null)))?((((map__69948.cljs$lang$protocol_mask$partition0$ & (64))) || (map__69948.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__69948):map__69948);
var bits_subset = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__69948__$1,cljs.core.cst$kw$value);
var map__69949 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69947,(4),null);
var map__69949__$1 = ((((!((map__69949 == null)))?((((map__69949.cljs$lang$protocol_mask$partition0$ & (64))) || (map__69949.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__69949):map__69949);
var response_c = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__69949__$1,cljs.core.cst$kw$ch);
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(response_c,(function (){var temp__4655__auto__ = find_model_pair(id);
if(cljs.core.truth_(temp__4655__auto__)){
var vec__69952 = temp__4655__auto__;
var prev_htm = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69952,(0),null);
var htm = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69952,(1),null);
var sense = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$senses,sense_id], null));
var ff_rgn_id = cljs.core.first(cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$fb_DASH_deps,sense_id], null)));
var prev_ff_rgn = (((org.nfrac.comportex.protocols.size(org.nfrac.comportex.protocols.ff_topology(sense)) > (0)))?cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(prev_htm,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,ff_rgn_id], null)):null);
var G__69953 = cljs.core.PersistentArrayMap.EMPTY;
var G__69953__$1 = ((cljs.core.contains_QMARK_(fetches,"active-bits"))?cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(G__69953,"active-bits",cljs.core.set(org.numenta.sanity.comportex.data.active_bits(sense))):G__69953);
if(cljs.core.truth_((function (){var and__6141__auto__ = cljs.core.contains_QMARK_(fetches,"pred-bits-alpha");
if(and__6141__auto__){
return prev_ff_rgn;
} else {
return and__6141__auto__;
}
})())){
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(G__69953__$1,"pred-bits-alpha",(function (){var start = org.nfrac.comportex.core.ff_base(htm,ff_rgn_id,sense_id);
var end = (start + org.nfrac.comportex.protocols.size(org.nfrac.comportex.protocols.ff_topology(sense)));
return org.nfrac.comportex.util.remap(((function (start,end,G__69953,G__69953__$1,sense,ff_rgn_id,prev_ff_rgn,vec__69952,prev_htm,htm,temp__4655__auto__,vec__69947,id,sense_id,fetches,map__69948,map__69948__$1,bits_subset,map__69949,map__69949__$1,response_c,G__69911,client_info,vec__69908,vec__69909,command,xs,client_id){
return (function (p1__69587_SHARP_){
var x__6491__auto__ = 1.0;
var y__6492__auto__ = (p1__69587_SHARP_ / (8));
return ((x__6491__auto__ < y__6492__auto__) ? x__6491__auto__ : y__6492__auto__);
});})(start,end,G__69953,G__69953__$1,sense,ff_rgn_id,prev_ff_rgn,vec__69952,prev_htm,htm,temp__4655__auto__,vec__69947,id,sense_id,fetches,map__69948,map__69948__$1,bits_subset,map__69949,map__69949__$1,response_c,G__69911,client_info,vec__69908,vec__69909,command,xs,client_id))
,cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,cljs.core.keep.cljs$core$IFn$_invoke$arity$2(((function (start,end,G__69953,G__69953__$1,sense,ff_rgn_id,prev_ff_rgn,vec__69952,prev_htm,htm,temp__4655__auto__,vec__69947,id,sense_id,fetches,map__69948,map__69948__$1,bits_subset,map__69949,map__69949__$1,response_c,G__69911,client_info,vec__69908,vec__69909,command,xs,client_id){
return (function (p__69954){
var vec__69955 = p__69954;
var id__$1 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69955,(0),null);
var votes = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69955,(1),null);
if(((start <= id__$1)) && ((id__$1 < end))){
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(id__$1 - start),votes], null);
} else {
return null;
}
});})(start,end,G__69953,G__69953__$1,sense,ff_rgn_id,prev_ff_rgn,vec__69952,prev_htm,htm,temp__4655__auto__,vec__69947,id,sense_id,fetches,map__69948,map__69948__$1,bits_subset,map__69949,map__69949__$1,response_c,G__69911,client_info,vec__69908,vec__69909,command,xs,client_id))
,org.nfrac.comportex.core.predicted_bit_votes(prev_ff_rgn))));
})());
} else {
return G__69953__$1;
}
} else {
return org.numenta.sanity.comportex.journal.id_missing_response(id,steps_offset);
}
})());

break;
case "get-proximal-synapses-by-source-bit":
var vec__69956 = xs;
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69956,(0),null);
var sense_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69956,(1),null);
var bit = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69956,(2),null);
var syn_states = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69956,(3),null);
var map__69957 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69956,(4),null);
var map__69957__$1 = ((((!((map__69957 == null)))?((((map__69957.cljs$lang$protocol_mask$partition0$ & (64))) || (map__69957.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__69957):map__69957);
var response_c = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__69957__$1,cljs.core.cst$kw$ch);
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(response_c,(function (){var temp__4655__auto__ = find_model(id);
if(cljs.core.truth_(temp__4655__auto__)){
var htm = temp__4655__auto__;
return org.numenta.sanity.comportex.data.syns_from_source_bit(htm,sense_id,bit,syn_states);
} else {
return org.numenta.sanity.comportex.journal.id_missing_response(id,steps_offset);
}
})());

break;
case "get-column-cells":
var vec__69959 = xs;
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69959,(0),null);
var rgn_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69959,(1),null);
var lyr_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69959,(2),null);
var col = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69959,(3),null);
var fetches = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69959,(4),null);
var map__69960 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69959,(5),null);
var map__69960__$1 = ((((!((map__69960 == null)))?((((map__69960.cljs$lang$protocol_mask$partition0$ & (64))) || (map__69960.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__69960):map__69960);
var response_c = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__69960__$1,cljs.core.cst$kw$ch);
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(response_c,(function (){var temp__4655__auto__ = find_model(id);
if(cljs.core.truth_(temp__4655__auto__)){
var htm = temp__4655__auto__;
var lyr = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,rgn_id,lyr_id], null));
var extract_cells = ((function (lyr,htm,temp__4655__auto__,vec__69959,id,rgn_id,lyr_id,col,fetches,map__69960,map__69960__$1,response_c,G__69911,client_info,vec__69908,vec__69909,command,xs,client_id){
return (function (p1__69588_SHARP_){
return cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentHashSet.EMPTY,cljs.core.keep.cljs$core$IFn$_invoke$arity$2(((function (lyr,htm,temp__4655__auto__,vec__69959,id,rgn_id,lyr_id,col,fetches,map__69960,map__69960__$1,response_c,G__69911,client_info,vec__69908,vec__69909,command,xs,client_id){
return (function (p__69962){
var vec__69963 = p__69962;
var column = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69963,(0),null);
var ci = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69963,(1),null);
if(cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(col,column)){
return ci;
} else {
return null;
}
});})(lyr,htm,temp__4655__auto__,vec__69959,id,rgn_id,lyr_id,col,fetches,map__69960,map__69960__$1,response_c,G__69911,client_info,vec__69908,vec__69909,command,xs,client_id))
,p1__69588_SHARP_));
});})(lyr,htm,temp__4655__auto__,vec__69959,id,rgn_id,lyr_id,col,fetches,map__69960,map__69960__$1,response_c,G__69911,client_info,vec__69908,vec__69909,command,xs,client_id))
;
var G__69964 = cljs.core.PersistentArrayMap.EMPTY;
var G__69964__$1 = ((cljs.core.contains_QMARK_(fetches,"active-cells"))?cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(G__69964,"active-cells",extract_cells(org.nfrac.comportex.protocols.active_cells(lyr))):G__69964);
var G__69964__$2 = ((cljs.core.contains_QMARK_(fetches,"prior-predicted-cells"))?cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(G__69964__$1,"prior-predicted-cells",extract_cells(org.nfrac.comportex.protocols.prior_predictive_cells(lyr))):G__69964__$1);
if(cljs.core.contains_QMARK_(fetches,"winner-cells")){
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(G__69964__$2,"winner-cells",extract_cells(org.nfrac.comportex.protocols.winner_cells(lyr)));
} else {
return G__69964__$2;
}
} else {
return org.numenta.sanity.comportex.journal.id_missing_response(id,steps_offset);
}
})());

break;
case "get-apical-segments":
var vec__69965 = xs;
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69965,(0),null);
var rgn_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69965,(1),null);
var lyr_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69965,(2),null);
var seg_selector = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69965,(3),null);
var map__69966 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69965,(4),null);
var map__69966__$1 = ((((!((map__69966 == null)))?((((map__69966.cljs$lang$protocol_mask$partition0$ & (64))) || (map__69966.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__69966):map__69966);
var response_c = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__69966__$1,cljs.core.cst$kw$ch);
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(response_c,(function (){var temp__4655__auto__ = find_model_pair(id);
if(cljs.core.truth_(temp__4655__auto__)){
var vec__69968 = temp__4655__auto__;
var prev_htm = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69968,(0),null);
var htm = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69968,(1),null);
return org.numenta.sanity.comportex.data.query_segs(htm,prev_htm,rgn_id,lyr_id,seg_selector,cljs.core.cst$kw$apical);
} else {
return org.numenta.sanity.comportex.journal.id_missing_response(id,steps_offset);
}
})());

break;
case "get-distal-segments":
var vec__69969 = xs;
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69969,(0),null);
var rgn_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69969,(1),null);
var lyr_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69969,(2),null);
var seg_selector = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69969,(3),null);
var map__69970 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69969,(4),null);
var map__69970__$1 = ((((!((map__69970 == null)))?((((map__69970.cljs$lang$protocol_mask$partition0$ & (64))) || (map__69970.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__69970):map__69970);
var response_c = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__69970__$1,cljs.core.cst$kw$ch);
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(response_c,(function (){var temp__4655__auto__ = find_model_pair(id);
if(cljs.core.truth_(temp__4655__auto__)){
var vec__69972 = temp__4655__auto__;
var prev_htm = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69972,(0),null);
var htm = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69972,(1),null);
return org.numenta.sanity.comportex.data.query_segs(htm,prev_htm,rgn_id,lyr_id,seg_selector,cljs.core.cst$kw$distal);
} else {
return org.numenta.sanity.comportex.journal.id_missing_response(id,steps_offset);
}
})());

break;
case "get-proximal-segments":
var vec__69973 = xs;
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69973,(0),null);
var rgn_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69973,(1),null);
var lyr_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69973,(2),null);
var seg_selector = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69973,(3),null);
var map__69974 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69973,(4),null);
var map__69974__$1 = ((((!((map__69974 == null)))?((((map__69974.cljs$lang$protocol_mask$partition0$ & (64))) || (map__69974.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__69974):map__69974);
var response_c = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__69974__$1,cljs.core.cst$kw$ch);
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(response_c,(function (){var temp__4655__auto__ = find_model_pair(id);
if(cljs.core.truth_(temp__4655__auto__)){
var vec__69976 = temp__4655__auto__;
var prev_htm = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69976,(0),null);
var htm = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69976,(1),null);
return org.numenta.sanity.comportex.data.query_segs(htm,prev_htm,rgn_id,lyr_id,seg_selector,cljs.core.cst$kw$proximal);
} else {
return org.numenta.sanity.comportex.journal.id_missing_response(id,steps_offset);
}
})());

break;
case "get-apical-synapses":
var vec__69977 = xs;
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69977,(0),null);
var rgn_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69977,(1),null);
var lyr_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69977,(2),null);
var seg_selector = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69977,(3),null);
var syn_states = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69977,(4),null);
var map__69978 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69977,(5),null);
var map__69978__$1 = ((((!((map__69978 == null)))?((((map__69978.cljs$lang$protocol_mask$partition0$ & (64))) || (map__69978.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__69978):map__69978);
var response_c = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__69978__$1,cljs.core.cst$kw$ch);
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(response_c,(function (){var temp__4655__auto__ = find_model_pair(id);
if(cljs.core.truth_(temp__4655__auto__)){
var vec__69980 = temp__4655__auto__;
var prev_htm = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69980,(0),null);
var htm = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69980,(1),null);
return org.numenta.sanity.comportex.data.query_syns(htm,prev_htm,rgn_id,lyr_id,seg_selector,syn_states,cljs.core.cst$kw$apical);
} else {
return org.numenta.sanity.comportex.journal.id_missing_response(id,steps_offset);
}
})());

break;
case "get-distal-synapses":
var vec__69981 = xs;
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69981,(0),null);
var rgn_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69981,(1),null);
var lyr_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69981,(2),null);
var seg_selector = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69981,(3),null);
var syn_states = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69981,(4),null);
var map__69982 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69981,(5),null);
var map__69982__$1 = ((((!((map__69982 == null)))?((((map__69982.cljs$lang$protocol_mask$partition0$ & (64))) || (map__69982.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__69982):map__69982);
var response_c = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__69982__$1,cljs.core.cst$kw$ch);
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(response_c,(function (){var temp__4655__auto__ = find_model_pair(id);
if(cljs.core.truth_(temp__4655__auto__)){
var vec__69984 = temp__4655__auto__;
var prev_htm = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69984,(0),null);
var htm = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69984,(1),null);
return org.numenta.sanity.comportex.data.query_syns(htm,prev_htm,rgn_id,lyr_id,seg_selector,syn_states,cljs.core.cst$kw$distal);
} else {
return org.numenta.sanity.comportex.journal.id_missing_response(id,steps_offset);
}
})());

break;
case "get-proximal-synapses":
var vec__69985 = xs;
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69985,(0),null);
var rgn_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69985,(1),null);
var lyr_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69985,(2),null);
var seg_selector = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69985,(3),null);
var syn_states = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69985,(4),null);
var map__69986 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69985,(5),null);
var map__69986__$1 = ((((!((map__69986 == null)))?((((map__69986.cljs$lang$protocol_mask$partition0$ & (64))) || (map__69986.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__69986):map__69986);
var response_c = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__69986__$1,cljs.core.cst$kw$ch);
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(response_c,(function (){var temp__4655__auto__ = find_model_pair(id);
if(cljs.core.truth_(temp__4655__auto__)){
var vec__69988 = temp__4655__auto__;
var prev_htm = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69988,(0),null);
var htm = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69988,(1),null);
return org.numenta.sanity.comportex.data.query_syns(htm,prev_htm,rgn_id,lyr_id,seg_selector,syn_states,cljs.core.cst$kw$proximal);
} else {
return org.numenta.sanity.comportex.journal.id_missing_response(id,steps_offset);
}
})());

break;
case "get-details-text":
var vec__69989 = xs;
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69989,(0),null);
var rgn_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69989,(1),null);
var lyr_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69989,(2),null);
var col = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69989,(3),null);
var map__69990 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69989,(4),null);
var map__69990__$1 = ((((!((map__69990 == null)))?((((map__69990.cljs$lang$protocol_mask$partition0$ & (64))) || (map__69990.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__69990):map__69990);
var response_c = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__69990__$1,cljs.core.cst$kw$ch);
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(response_c,(function (){var temp__4655__auto__ = find_model_pair(id);
if(cljs.core.truth_(temp__4655__auto__)){
var vec__69992 = temp__4655__auto__;
var prev_htm = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69992,(0),null);
var htm = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69992,(1),null);
return org.numenta.sanity.comportex.details.detail_text(htm,prev_htm,rgn_id,lyr_id,col);
} else {
return org.numenta.sanity.comportex.journal.id_missing_response(id,steps_offset);
}
})());

break;
case "get-model":
var vec__69993 = xs;
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69993,(0),null);
var map__69994 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69993,(1),null);
var map__69994__$1 = ((((!((map__69994 == null)))?((((map__69994.cljs$lang$protocol_mask$partition0$ & (64))) || (map__69994.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__69994):map__69994);
var response_c = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__69994__$1,cljs.core.cst$kw$ch);
var as_str_QMARK_ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69993,(2),null);
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(response_c,(function (){var temp__4655__auto__ = find_model(id);
if(cljs.core.truth_(temp__4655__auto__)){
var htm = temp__4655__auto__;
var G__69996 = htm;
if(cljs.core.truth_(as_str_QMARK_)){
return cljs.core.pr_str.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([G__69996], 0));
} else {
return G__69996;
}
} else {
return org.numenta.sanity.comportex.journal.id_missing_response(id,steps_offset);
}
})());

break;
case "get-layer-stats":
var vec__69997 = xs;
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69997,(0),null);
var rgn_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69997,(1),null);
var lyr_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69997,(2),null);
var fetches = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69997,(3),null);
var map__69998 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__69997,(4),null);
var map__69998__$1 = ((((!((map__69998 == null)))?((((map__69998.cljs$lang$protocol_mask$partition0$ & (64))) || (map__69998.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__69998):map__69998);
var response_c = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__69998__$1,cljs.core.cst$kw$ch);
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(response_c,(function (){var temp__4655__auto__ = find_model(id);
if(cljs.core.truth_(temp__4655__auto__)){
var htm = temp__4655__auto__;
var lyr = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,rgn_id,lyr_id], null));
var a_cols = org.nfrac.comportex.protocols.active_columns(lyr);
var ppc = org.nfrac.comportex.protocols.prior_predictive_cells(lyr);
var pp_cols = cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentHashSet.EMPTY,cljs.core.map.cljs$core$IFn$_invoke$arity$2(cljs.core.first,ppc));
var ap_cols = clojure.set.intersection.cljs$core$IFn$_invoke$arity$2(pp_cols,a_cols);
var col_states = cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([cljs.core.zipmap(pp_cols,cljs.core.repeat.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$predicted)),cljs.core.zipmap(a_cols,cljs.core.repeat.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$active)),cljs.core.zipmap(ap_cols,cljs.core.repeat.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$active_DASH_predicted))], 0));
var freqs = cljs.core.frequencies(cljs.core.vals(col_states));
var G__70000 = cljs.core.PersistentArrayMap.EMPTY;
var G__70000__$1 = ((cljs.core.contains_QMARK_(fetches,"n-unpredicted-active-columns"))?cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(G__70000,"n-unpredicted-active-columns",cljs.core.get.cljs$core$IFn$_invoke$arity$3(freqs,cljs.core.cst$kw$active,(0))):G__70000);
var G__70000__$2 = ((cljs.core.contains_QMARK_(fetches,"n-predicted-inactive-columns"))?cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(G__70000__$1,"n-predicted-inactive-columns",cljs.core.get.cljs$core$IFn$_invoke$arity$3(freqs,cljs.core.cst$kw$predicted,(0))):G__70000__$1);
if(cljs.core.contains_QMARK_(fetches,"n-predicted-active-columns")){
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(G__70000__$2,"n-predicted-active-columns",cljs.core.get.cljs$core$IFn$_invoke$arity$3(freqs,cljs.core.cst$kw$active_DASH_predicted,(0)));
} else {
return G__70000__$2;
}
} else {
return org.numenta.sanity.comportex.journal.id_missing_response(id,steps_offset);
}
})());

break;
case "get-cell-excitation-data":
var vec__70001 = xs;
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70001,(0),null);
var rgn_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70001,(1),null);
var lyr_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70001,(2),null);
var sel_col = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70001,(3),null);
var map__70002 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70001,(4),null);
var map__70002__$1 = ((((!((map__70002 == null)))?((((map__70002.cljs$lang$protocol_mask$partition0$ & (64))) || (map__70002.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__70002):map__70002);
var response_c = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__70002__$1,cljs.core.cst$kw$ch);
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(response_c,(function (){var vec__70004 = find_model_pair(id);
var prev_htm = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70004,(0),null);
var htm = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70004,(1),null);
if(cljs.core.truth_(prev_htm)){
return org.numenta.sanity.comportex.data.cell_excitation_data(htm,prev_htm,rgn_id,lyr_id,sel_col);
} else {
return org.numenta.sanity.comportex.journal.id_missing_response(id,steps_offset);
}
})());

break;
case "get-cells-by-state":
var vec__70005 = xs;
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70005,(0),null);
var rgn_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70005,(1),null);
var lyr_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70005,(2),null);
var map__70006 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70005,(3),null);
var map__70006__$1 = ((((!((map__70006 == null)))?((((map__70006.cljs$lang$protocol_mask$partition0$ & (64))) || (map__70006.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__70006):map__70006);
var response_c = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__70006__$1,cljs.core.cst$kw$ch);
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(response_c,(function (){var temp__4655__auto__ = find_model(id);
if(cljs.core.truth_(temp__4655__auto__)){
var htm = temp__4655__auto__;
var layer = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,rgn_id,lyr_id], null));
return new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$winner_DASH_cells,org.nfrac.comportex.protocols.winner_cells(layer),cljs.core.cst$kw$active_DASH_cells,org.nfrac.comportex.protocols.active_cells(layer),cljs.core.cst$kw$pred_DASH_cells,org.nfrac.comportex.protocols.predictive_cells(layer),cljs.core.cst$kw$engaged_QMARK_,true], null);
} else {
return org.numenta.sanity.comportex.journal.id_missing_response(id,steps_offset);
}
})());

break;
case "get-transitions-data":
var vec__70008 = xs;
var id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70008,(0),null);
var rgn_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70008,(1),null);
var lyr_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70008,(2),null);
var cell_sdr_fracs = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70008,(3),null);
var map__70009 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__70008,(4),null);
var map__70009__$1 = ((((!((map__70009 == null)))?((((map__70009.cljs$lang$protocol_mask$partition0$ & (64))) || (map__70009.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__70009):map__70009);
var response_c = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__70009__$1,cljs.core.cst$kw$ch);
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(response_c,(function (){var temp__4655__auto__ = find_model(id);
if(cljs.core.truth_(temp__4655__auto__)){
var htm = temp__4655__auto__;
return org.numenta.sanity.comportex.data.transitions_data(htm,rgn_id,lyr_id,cell_sdr_fracs);
} else {
return org.numenta.sanity.comportex.journal.id_missing_response(id,steps_offset);
}
})());

break;
default:
throw (new Error([cljs.core.str("No matching clause: "),cljs.core.str(command)].join('')));

}
});
});
org.numenta.sanity.comportex.journal.init = (function org$numenta$sanity$comportex$journal$init(steps_c,commands_c,current_model,n_keep){
var steps_offset = (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1((0)) : cljs.core.atom.call(null,(0)));
var model_steps = (function (){var G__70113 = cljs.core.PersistentVector.EMPTY;
return (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(G__70113) : cljs.core.atom.call(null,G__70113));
})();
var steps_in = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
var steps_mult = cljs.core.async.mult(steps_in);
var client_infos = (function (){var G__70114 = cljs.core.PersistentArrayMap.EMPTY;
return (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(G__70114) : cljs.core.atom.call(null,G__70114));
})();
var capture_options = (function (){var G__70115 = new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$keep_DASH_steps,n_keep,cljs.core.cst$kw$ff_DASH_synapses,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$capture_QMARK_,true,cljs.core.cst$kw$only_DASH_active_QMARK_,false,cljs.core.cst$kw$only_DASH_connected_QMARK_,false], null),cljs.core.cst$kw$distal_DASH_synapses,new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$capture_QMARK_,true,cljs.core.cst$kw$only_DASH_active_QMARK_,false,cljs.core.cst$kw$only_DASH_connected_QMARK_,false,cljs.core.cst$kw$only_DASH_noteworthy_DASH_columns_QMARK_,false], null),cljs.core.cst$kw$apical_DASH_synapses,new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$capture_QMARK_,true,cljs.core.cst$kw$only_DASH_active_QMARK_,false,cljs.core.cst$kw$only_DASH_connected_QMARK_,false,cljs.core.cst$kw$only_DASH_noteworthy_DASH_columns_QMARK_,false], null)], null);
return (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(G__70115) : cljs.core.atom.call(null,G__70115));
})();
var handle_command = org.numenta.sanity.comportex.journal.command_handler(current_model,steps_offset,model_steps,steps_mult,client_infos,capture_options);
var c__38109__auto___70214 = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto___70214,steps_offset,model_steps,steps_in,steps_mult,client_infos,capture_options,handle_command){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto___70214,steps_offset,model_steps,steps_in,steps_mult,client_infos,capture_options,handle_command){
return (function (state_70155){
var state_val_70156 = (state_70155[(1)]);
if((state_val_70156 === (7))){
var inst_70151 = (state_70155[(2)]);
var state_70155__$1 = state_70155;
var statearr_70157_70215 = state_70155__$1;
(statearr_70157_70215[(2)] = inst_70151);

(statearr_70157_70215[(1)] = (3));


return cljs.core.cst$kw$recur;
} else {
if((state_val_70156 === (1))){
var state_70155__$1 = state_70155;
var statearr_70158_70216 = state_70155__$1;
(statearr_70158_70216[(2)] = null);

(statearr_70158_70216[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_70156 === (4))){
var inst_70118 = (state_70155[(7)]);
var inst_70118__$1 = (state_70155[(2)]);
var state_70155__$1 = (function (){var statearr_70159 = state_70155;
(statearr_70159[(7)] = inst_70118__$1);

return statearr_70159;
})();
if(cljs.core.truth_(inst_70118__$1)){
var statearr_70160_70217 = state_70155__$1;
(statearr_70160_70217[(1)] = (5));

} else {
var statearr_70161_70218 = state_70155__$1;
(statearr_70161_70218[(1)] = (6));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_70156 === (13))){
var inst_70123 = (state_70155[(8)]);
var inst_70136 = (state_70155[(9)]);
var inst_70118 = (state_70155[(7)]);
var inst_70143 = (state_70155[(2)]);
var inst_70144 = (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(model_steps,inst_70143) : cljs.core.reset_BANG_.call(null,model_steps,inst_70143));
var inst_70145 = cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$3(steps_offset,cljs.core._PLUS_,inst_70136);
var inst_70146 = org.numenta.sanity.comportex.journal.make_step(inst_70118,inst_70123);
var inst_70147 = cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(steps_in,inst_70146);
var state_70155__$1 = (function (){var statearr_70162 = state_70155;
(statearr_70162[(10)] = inst_70145);

(statearr_70162[(11)] = inst_70147);

(statearr_70162[(12)] = inst_70144);

return statearr_70162;
})();
var statearr_70163_70219 = state_70155__$1;
(statearr_70163_70219[(2)] = null);

(statearr_70163_70219[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_70156 === (6))){
var state_70155__$1 = state_70155;
var statearr_70164_70220 = state_70155__$1;
(statearr_70164_70220[(2)] = null);

(statearr_70164_70220[(1)] = (7));


return cljs.core.cst$kw$recur;
} else {
if((state_val_70156 === (3))){
var inst_70153 = (state_70155[(2)]);
var state_70155__$1 = state_70155;
return cljs.core.async.impl.ioc_helpers.return_chan(state_70155__$1,inst_70153);
} else {
if((state_val_70156 === (12))){
var inst_70125 = (state_70155[(13)]);
var state_70155__$1 = state_70155;
var statearr_70165_70221 = state_70155__$1;
(statearr_70165_70221[(2)] = inst_70125);

(statearr_70165_70221[(1)] = (13));


return cljs.core.cst$kw$recur;
} else {
if((state_val_70156 === (2))){
var state_70155__$1 = state_70155;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_70155__$1,(4),steps_c);
} else {
if((state_val_70156 === (11))){
var inst_70125 = (state_70155[(13)]);
var inst_70136 = (state_70155[(9)]);
var inst_70140 = cljs.core.subvec.cljs$core$IFn$_invoke$arity$2(inst_70125,inst_70136);
var state_70155__$1 = state_70155;
var statearr_70166_70222 = state_70155__$1;
(statearr_70166_70222[(2)] = inst_70140);

(statearr_70166_70222[(1)] = (13));


return cljs.core.cst$kw$recur;
} else {
if((state_val_70156 === (9))){
var state_70155__$1 = state_70155;
var statearr_70167_70223 = state_70155__$1;
(statearr_70167_70223[(2)] = (0));

(statearr_70167_70223[(1)] = (10));


return cljs.core.cst$kw$recur;
} else {
if((state_val_70156 === (5))){
var inst_70127 = (state_70155[(14)]);
var inst_70118 = (state_70155[(7)]);
var inst_70120 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(steps_offset) : cljs.core.deref.call(null,steps_offset));
var inst_70121 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(model_steps) : cljs.core.deref.call(null,model_steps));
var inst_70122 = cljs.core.count(inst_70121);
var inst_70123 = (inst_70120 + inst_70122);
var inst_70124 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(model_steps) : cljs.core.deref.call(null,model_steps));
var inst_70125 = cljs.core.conj.cljs$core$IFn$_invoke$arity$2(inst_70124,inst_70118);
var inst_70126 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(capture_options) : cljs.core.deref.call(null,capture_options));
var inst_70127__$1 = cljs.core.cst$kw$keep_DASH_steps.cljs$core$IFn$_invoke$arity$1(inst_70126);
var inst_70128 = (inst_70127__$1 < (0));
var inst_70129 = cljs.core.not(inst_70128);
var state_70155__$1 = (function (){var statearr_70168 = state_70155;
(statearr_70168[(8)] = inst_70123);

(statearr_70168[(13)] = inst_70125);

(statearr_70168[(14)] = inst_70127__$1);

return statearr_70168;
})();
if(inst_70129){
var statearr_70169_70224 = state_70155__$1;
(statearr_70169_70224[(1)] = (8));

} else {
var statearr_70170_70225 = state_70155__$1;
(statearr_70170_70225[(1)] = (9));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_70156 === (10))){
var inst_70136 = (state_70155[(9)]);
var inst_70136__$1 = (state_70155[(2)]);
var inst_70138 = (inst_70136__$1 > (0));
var state_70155__$1 = (function (){var statearr_70171 = state_70155;
(statearr_70171[(9)] = inst_70136__$1);

return statearr_70171;
})();
if(cljs.core.truth_(inst_70138)){
var statearr_70172_70226 = state_70155__$1;
(statearr_70172_70226[(1)] = (11));

} else {
var statearr_70173_70227 = state_70155__$1;
(statearr_70173_70227[(1)] = (12));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_70156 === (8))){
var inst_70125 = (state_70155[(13)]);
var inst_70127 = (state_70155[(14)]);
var inst_70131 = cljs.core.count(inst_70125);
var inst_70132 = (inst_70131 - inst_70127);
var inst_70133 = (((0) > inst_70132) ? (0) : inst_70132);
var state_70155__$1 = state_70155;
var statearr_70174_70228 = state_70155__$1;
(statearr_70174_70228[(2)] = inst_70133);

(statearr_70174_70228[(1)] = (10));


return cljs.core.cst$kw$recur;
} else {
return null;
}
}
}
}
}
}
}
}
}
}
}
}
}
});})(c__38109__auto___70214,steps_offset,model_steps,steps_in,steps_mult,client_infos,capture_options,handle_command))
;
return ((function (switch__37995__auto__,c__38109__auto___70214,steps_offset,model_steps,steps_in,steps_mult,client_infos,capture_options,handle_command){
return (function() {
var org$numenta$sanity$comportex$journal$init_$_state_machine__37996__auto__ = null;
var org$numenta$sanity$comportex$journal$init_$_state_machine__37996__auto____0 = (function (){
var statearr_70178 = [null,null,null,null,null,null,null,null,null,null,null,null,null,null,null];
(statearr_70178[(0)] = org$numenta$sanity$comportex$journal$init_$_state_machine__37996__auto__);

(statearr_70178[(1)] = (1));

return statearr_70178;
});
var org$numenta$sanity$comportex$journal$init_$_state_machine__37996__auto____1 = (function (state_70155){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_70155);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e70179){if((e70179 instanceof Object)){
var ex__37999__auto__ = e70179;
var statearr_70180_70229 = state_70155;
(statearr_70180_70229[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_70155);

return cljs.core.cst$kw$recur;
} else {
throw e70179;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__70230 = state_70155;
state_70155 = G__70230;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$comportex$journal$init_$_state_machine__37996__auto__ = function(state_70155){
switch(arguments.length){
case 0:
return org$numenta$sanity$comportex$journal$init_$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$comportex$journal$init_$_state_machine__37996__auto____1.call(this,state_70155);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$comportex$journal$init_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$comportex$journal$init_$_state_machine__37996__auto____0;
org$numenta$sanity$comportex$journal$init_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$comportex$journal$init_$_state_machine__37996__auto____1;
return org$numenta$sanity$comportex$journal$init_$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto___70214,steps_offset,model_steps,steps_in,steps_mult,client_infos,capture_options,handle_command))
})();
var state__38111__auto__ = (function (){var statearr_70181 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_70181[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto___70214);

return statearr_70181;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto___70214,steps_offset,model_steps,steps_in,steps_mult,client_infos,capture_options,handle_command))
);


var c__38109__auto__ = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto__,steps_offset,model_steps,steps_in,steps_mult,client_infos,capture_options,handle_command){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto__,steps_offset,model_steps,steps_in,steps_mult,client_infos,capture_options,handle_command){
return (function (state_70197){
var state_val_70198 = (state_70197[(1)]);
if((state_val_70198 === (1))){
var state_70197__$1 = state_70197;
var statearr_70199_70231 = state_70197__$1;
(statearr_70199_70231[(2)] = null);

(statearr_70199_70231[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_70198 === (2))){
var state_70197__$1 = state_70197;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_70197__$1,(4),commands_c);
} else {
if((state_val_70198 === (3))){
var inst_70195 = (state_70197[(2)]);
var state_70197__$1 = state_70197;
return cljs.core.async.impl.ioc_helpers.return_chan(state_70197__$1,inst_70195);
} else {
if((state_val_70198 === (4))){
var inst_70184 = (state_70197[(7)]);
var inst_70184__$1 = (state_70197[(2)]);
var inst_70185 = (inst_70184__$1 == null);
var inst_70186 = cljs.core.not(inst_70185);
var state_70197__$1 = (function (){var statearr_70200 = state_70197;
(statearr_70200[(7)] = inst_70184__$1);

return statearr_70200;
})();
if(inst_70186){
var statearr_70201_70232 = state_70197__$1;
(statearr_70201_70232[(1)] = (5));

} else {
var statearr_70202_70233 = state_70197__$1;
(statearr_70202_70233[(1)] = (6));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_70198 === (5))){
var inst_70184 = (state_70197[(7)]);
var inst_70188 = (handle_command.cljs$core$IFn$_invoke$arity$1 ? handle_command.cljs$core$IFn$_invoke$arity$1(inst_70184) : handle_command.call(null,inst_70184));
var state_70197__$1 = (function (){var statearr_70203 = state_70197;
(statearr_70203[(8)] = inst_70188);

return statearr_70203;
})();
var statearr_70204_70234 = state_70197__$1;
(statearr_70204_70234[(2)] = null);

(statearr_70204_70234[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_70198 === (6))){
var inst_70191 = cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["CLOSING JOURNAL"], 0));
var state_70197__$1 = state_70197;
var statearr_70205_70235 = state_70197__$1;
(statearr_70205_70235[(2)] = inst_70191);

(statearr_70205_70235[(1)] = (7));


return cljs.core.cst$kw$recur;
} else {
if((state_val_70198 === (7))){
var inst_70193 = (state_70197[(2)]);
var state_70197__$1 = state_70197;
var statearr_70206_70236 = state_70197__$1;
(statearr_70206_70236[(2)] = inst_70193);

(statearr_70206_70236[(1)] = (3));


return cljs.core.cst$kw$recur;
} else {
return null;
}
}
}
}
}
}
}
});})(c__38109__auto__,steps_offset,model_steps,steps_in,steps_mult,client_infos,capture_options,handle_command))
;
return ((function (switch__37995__auto__,c__38109__auto__,steps_offset,model_steps,steps_in,steps_mult,client_infos,capture_options,handle_command){
return (function() {
var org$numenta$sanity$comportex$journal$init_$_state_machine__37996__auto__ = null;
var org$numenta$sanity$comportex$journal$init_$_state_machine__37996__auto____0 = (function (){
var statearr_70210 = [null,null,null,null,null,null,null,null,null];
(statearr_70210[(0)] = org$numenta$sanity$comportex$journal$init_$_state_machine__37996__auto__);

(statearr_70210[(1)] = (1));

return statearr_70210;
});
var org$numenta$sanity$comportex$journal$init_$_state_machine__37996__auto____1 = (function (state_70197){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_70197);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e70211){if((e70211 instanceof Object)){
var ex__37999__auto__ = e70211;
var statearr_70212_70237 = state_70197;
(statearr_70212_70237[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_70197);

return cljs.core.cst$kw$recur;
} else {
throw e70211;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__70238 = state_70197;
state_70197 = G__70238;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$comportex$journal$init_$_state_machine__37996__auto__ = function(state_70197){
switch(arguments.length){
case 0:
return org$numenta$sanity$comportex$journal$init_$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$comportex$journal$init_$_state_machine__37996__auto____1.call(this,state_70197);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$comportex$journal$init_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$comportex$journal$init_$_state_machine__37996__auto____0;
org$numenta$sanity$comportex$journal$init_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$comportex$journal$init_$_state_machine__37996__auto____1;
return org$numenta$sanity$comportex$journal$init_$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto__,steps_offset,model_steps,steps_in,steps_mult,client_infos,capture_options,handle_command))
})();
var state__38111__auto__ = (function (){var statearr_70213 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_70213[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto__);

return statearr_70213;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto__,steps_offset,model_steps,steps_in,steps_mult,client_infos,capture_options,handle_command))
);

return c__38109__auto__;
});
