// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.numenta.sanity.bridge.remote');
goog.require('cljs.core');
goog.require('cljs.core.async');
goog.require('cljs.pprint');
goog.require('cognitect.transit');
goog.require('org.numenta.sanity.bridge.marshalling');
goog.require('org.nfrac.comportex.topology');
org.numenta.sanity.bridge.remote.max_message_size = ((64) * (1024));
org.numenta.sanity.bridge.remote.transit_str = (function org$numenta$sanity$bridge$remote$transit_str(m,extra_handlers){
return cognitect.transit.write(cognitect.transit.writer.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.bridge.marshalling.encoding,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$handlers,extra_handlers], null)),m);
});
org.numenta.sanity.bridge.remote.read_transit_str = (function org$numenta$sanity$bridge$remote$read_transit_str(s,extra_handlers){
return cognitect.transit.read(cognitect.transit.reader.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.bridge.marshalling.encoding,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$handlers,extra_handlers], null)),s);
});
org.numenta.sanity.bridge.remote.target_put = (function org$numenta$sanity$bridge$remote$target_put(target,v){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, ["put!",target,v], null);
});
org.numenta.sanity.bridge.remote.target_close = (function org$numenta$sanity$bridge$remote$target_close(target){
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, ["close!",target], null);
});
org.numenta.sanity.bridge.remote.log_messages_QMARK_ = (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(false) : cljs.core.atom.call(null,false));
org.numenta.sanity.bridge.remote.log_raw_messages_QMARK_ = (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(false) : cljs.core.atom.call(null,false));
org.numenta.sanity.bridge.remote.log_pretty_QMARK_ = (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(true) : cljs.core.atom.call(null,true));
org.numenta.sanity.bridge.remote.log = (function org$numenta$sanity$bridge$remote$log(v,prefix){
cljs.core.pr.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([prefix], 0));

(cljs.core.truth_((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.bridge.remote.log_pretty_QMARK_) : cljs.core.deref.call(null,org.numenta.sanity.bridge.remote.log_pretty_QMARK_)))?cljs.pprint.pprint:cljs.core.println).call(null,v);

return v;
});
org.numenta.sanity.bridge.remote.connect_BANG_ = (function org$numenta$sanity$bridge$remote$connect_BANG_(connection_id,to_network_c,on_connect_c,ws_url,connecting_QMARK_,target__GT_mchannel){
var ws = (new WebSocket(ws_url));
var teardown_c = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
var connection_id_STAR_ = cljs.core.random_uuid();
var local_resources = (function (){var G__58799 = cljs.core.PersistentArrayMap.EMPTY;
return (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(G__58799) : cljs.core.atom.call(null,G__58799));
})();
var remote_resources = (function (){var G__58800 = cljs.core.PersistentArrayMap.EMPTY;
return (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(G__58800) : cljs.core.atom.call(null,G__58800));
})();
var G__58801 = ws;
(G__58801["onopen"] = ((function (G__58801,ws,teardown_c,connection_id_STAR_,local_resources,remote_resources){
return (function (evt){
cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["WebSocket connected."], 0));

(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(connection_id,connection_id_STAR_) : cljs.core.reset_BANG_.call(null,connection_id,connection_id_STAR_));

(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(connecting_QMARK_,false) : cljs.core.reset_BANG_.call(null,connecting_QMARK_,false));

var c__38109__auto___58985 = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto___58985,G__58801,ws,teardown_c,connection_id_STAR_,local_resources,remote_resources){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto___58985,G__58801,ws,teardown_c,connection_id_STAR_,local_resources,remote_resources){
return (function (state_58837){
var state_val_58838 = (state_58837[(1)]);
if((state_val_58838 === (7))){
var inst_58833 = (state_58837[(2)]);
var state_58837__$1 = state_58837;
var statearr_58839_58986 = state_58837__$1;
(statearr_58839_58986[(2)] = inst_58833);

(statearr_58839_58986[(1)] = (3));


return cljs.core.cst$kw$recur;
} else {
if((state_val_58838 === (1))){
var state_58837__$1 = state_58837;
var statearr_58840_58987 = state_58837__$1;
(statearr_58840_58987[(2)] = null);

(statearr_58840_58987[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_58838 === (4))){
var inst_58812 = (state_58837[(7)]);
var inst_58814 = (state_58837[(8)]);
var inst_58812__$1 = (state_58837[(2)]);
var inst_58813 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(inst_58812__$1,(0),null);
var inst_58814__$1 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(inst_58812__$1,(1),null);
var inst_58815 = cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(inst_58814__$1,teardown_c);
var state_58837__$1 = (function (){var statearr_58841 = state_58837;
(statearr_58841[(7)] = inst_58812__$1);

(statearr_58841[(9)] = inst_58813);

(statearr_58841[(8)] = inst_58814__$1);

return statearr_58841;
})();
if(inst_58815){
var statearr_58842_58988 = state_58837__$1;
(statearr_58842_58988[(1)] = (5));

} else {
var statearr_58843_58989 = state_58837__$1;
(statearr_58843_58989[(1)] = (6));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_58838 === (13))){
var inst_58829 = (state_58837[(2)]);
var state_58837__$1 = state_58837;
var statearr_58844_58990 = state_58837__$1;
(statearr_58844_58990[(2)] = inst_58829);

(statearr_58844_58990[(1)] = (10));


return cljs.core.cst$kw$recur;
} else {
if((state_val_58838 === (6))){
var inst_58814 = (state_58837[(8)]);
var inst_58818 = cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(inst_58814,on_connect_c);
var state_58837__$1 = state_58837;
if(inst_58818){
var statearr_58845_58991 = state_58837__$1;
(statearr_58845_58991[(1)] = (8));

} else {
var statearr_58846_58992 = state_58837__$1;
(statearr_58846_58992[(1)] = (9));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_58838 === (3))){
var inst_58835 = (state_58837[(2)]);
var state_58837__$1 = state_58837;
return cljs.core.async.impl.ioc_helpers.return_chan(state_58837__$1,inst_58835);
} else {
if((state_val_58838 === (12))){
var state_58837__$1 = state_58837;
var statearr_58847_58993 = state_58837__$1;
(statearr_58847_58993[(2)] = null);

(statearr_58847_58993[(1)] = (13));


return cljs.core.cst$kw$recur;
} else {
if((state_val_58838 === (2))){
var inst_58808 = cljs.core.PersistentVector.EMPTY_NODE;
var inst_58809 = [teardown_c,on_connect_c];
var inst_58810 = (new cljs.core.PersistentVector(null,2,(5),inst_58808,inst_58809,null));
var state_58837__$1 = state_58837;
return cljs.core.async.ioc_alts_BANG_.cljs$core$IFn$_invoke$arity$variadic(state_58837__$1,(4),inst_58810,cljs.core.array_seq([cljs.core.cst$kw$priority,true], 0));
} else {
if((state_val_58838 === (11))){
var inst_58813 = (state_58837[(9)]);
var state_58837__$1 = state_58837;
var statearr_58848_58994 = state_58837__$1;
(statearr_58848_58994[(2)] = inst_58813);

(statearr_58848_58994[(1)] = (13));


return cljs.core.cst$kw$recur;
} else {
if((state_val_58838 === (9))){
var inst_58814 = (state_58837[(8)]);
var inst_58825 = cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(inst_58814,cljs.core.cst$kw$default);
var state_58837__$1 = state_58837;
if(inst_58825){
var statearr_58849_58995 = state_58837__$1;
(statearr_58849_58995[(1)] = (11));

} else {
var statearr_58850_58996 = state_58837__$1;
(statearr_58850_58996[(1)] = (12));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_58838 === (5))){
var state_58837__$1 = state_58837;
var statearr_58851_58997 = state_58837__$1;
(statearr_58851_58997[(2)] = null);

(statearr_58851_58997[(1)] = (7));


return cljs.core.cst$kw$recur;
} else {
if((state_val_58838 === (10))){
var inst_58831 = (state_58837[(2)]);
var state_58837__$1 = state_58837;
var statearr_58852_58998 = state_58837__$1;
(statearr_58852_58998[(2)] = inst_58831);

(statearr_58852_58998[(1)] = (7));


return cljs.core.cst$kw$recur;
} else {
if((state_val_58838 === (8))){
var inst_58812 = (state_58837[(7)]);
var inst_58821 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(inst_58812,(0),null);
var inst_58822 = (inst_58821.cljs$core$IFn$_invoke$arity$0 ? inst_58821.cljs$core$IFn$_invoke$arity$0() : inst_58821.call(null));
var state_58837__$1 = (function (){var statearr_58853 = state_58837;
(statearr_58853[(10)] = inst_58822);

return statearr_58853;
})();
var statearr_58854_58999 = state_58837__$1;
(statearr_58854_58999[(2)] = null);

(statearr_58854_58999[(1)] = (2));


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
});})(c__38109__auto___58985,G__58801,ws,teardown_c,connection_id_STAR_,local_resources,remote_resources))
;
return ((function (switch__37995__auto__,c__38109__auto___58985,G__58801,ws,teardown_c,connection_id_STAR_,local_resources,remote_resources){
return (function() {
var org$numenta$sanity$bridge$remote$connect_BANG__$_state_machine__37996__auto__ = null;
var org$numenta$sanity$bridge$remote$connect_BANG__$_state_machine__37996__auto____0 = (function (){
var statearr_58858 = [null,null,null,null,null,null,null,null,null,null,null];
(statearr_58858[(0)] = org$numenta$sanity$bridge$remote$connect_BANG__$_state_machine__37996__auto__);

(statearr_58858[(1)] = (1));

return statearr_58858;
});
var org$numenta$sanity$bridge$remote$connect_BANG__$_state_machine__37996__auto____1 = (function (state_58837){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_58837);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e58859){if((e58859 instanceof Object)){
var ex__37999__auto__ = e58859;
var statearr_58860_59000 = state_58837;
(statearr_58860_59000[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_58837);

return cljs.core.cst$kw$recur;
} else {
throw e58859;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__59001 = state_58837;
state_58837 = G__59001;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$bridge$remote$connect_BANG__$_state_machine__37996__auto__ = function(state_58837){
switch(arguments.length){
case 0:
return org$numenta$sanity$bridge$remote$connect_BANG__$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$bridge$remote$connect_BANG__$_state_machine__37996__auto____1.call(this,state_58837);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$bridge$remote$connect_BANG__$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$bridge$remote$connect_BANG__$_state_machine__37996__auto____0;
org$numenta$sanity$bridge$remote$connect_BANG__$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$bridge$remote$connect_BANG__$_state_machine__37996__auto____1;
return org$numenta$sanity$bridge$remote$connect_BANG__$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto___58985,G__58801,ws,teardown_c,connection_id_STAR_,local_resources,remote_resources))
})();
var state__38111__auto__ = (function (){var statearr_58861 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_58861[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto___58985);

return statearr_58861;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto___58985,G__58801,ws,teardown_c,connection_id_STAR_,local_resources,remote_resources))
);


var c__38109__auto__ = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto__,G__58801,ws,teardown_c,connection_id_STAR_,local_resources,remote_resources){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto__,G__58801,ws,teardown_c,connection_id_STAR_,local_resources,remote_resources){
return (function (state_58930){
var state_val_58931 = (state_58930[(1)]);
if((state_val_58931 === (7))){
var inst_58891 = (state_58930[(7)]);
var inst_58891__$1 = (state_58930[(2)]);
var inst_58892 = (inst_58891__$1 == null);
var state_58930__$1 = (function (){var statearr_58932 = state_58930;
(statearr_58932[(7)] = inst_58891__$1);

return statearr_58932;
})();
if(cljs.core.truth_(inst_58892)){
var statearr_58933_59002 = state_58930__$1;
(statearr_58933_59002[(1)] = (14));

} else {
var statearr_58934_59003 = state_58930__$1;
(statearr_58934_59003[(1)] = (15));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_58931 === (20))){
var inst_58901 = (state_58930[(8)]);
var inst_58903 = org.numenta.sanity.bridge.marshalling.write_handlers(target__GT_mchannel,local_resources);
var inst_58904 = org.numenta.sanity.bridge.remote.transit_str(inst_58901,inst_58903);
var state_58930__$1 = state_58930;
var statearr_58935_59004 = state_58930__$1;
(statearr_58935_59004[(2)] = inst_58904);

(statearr_58935_59004[(1)] = (22));


return cljs.core.cst$kw$recur;
} else {
if((state_val_58931 === (27))){
var state_58930__$1 = state_58930;
var statearr_58936_59005 = state_58930__$1;
(statearr_58936_59005[(2)] = null);

(statearr_58936_59005[(1)] = (28));


return cljs.core.cst$kw$recur;
} else {
if((state_val_58931 === (1))){
var state_58930__$1 = state_58930;
var statearr_58937_59006 = state_58930__$1;
(statearr_58937_59006[(2)] = null);

(statearr_58937_59006[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_58931 === (24))){
var inst_58907 = (state_58930[(9)]);
var state_58930__$1 = state_58930;
var statearr_58938_59007 = state_58930__$1;
(statearr_58938_59007[(2)] = inst_58907);

(statearr_58938_59007[(1)] = (25));


return cljs.core.cst$kw$recur;
} else {
if((state_val_58931 === (4))){
var inst_58874 = (state_58930[(10)]);
var inst_58872 = (state_58930[(11)]);
var inst_58872__$1 = (state_58930[(2)]);
var inst_58873 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(inst_58872__$1,(0),null);
var inst_58874__$1 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(inst_58872__$1,(1),null);
var inst_58875 = cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(inst_58874__$1,teardown_c);
var state_58930__$1 = (function (){var statearr_58939 = state_58930;
(statearr_58939[(10)] = inst_58874__$1);

(statearr_58939[(12)] = inst_58873);

(statearr_58939[(11)] = inst_58872__$1);

return statearr_58939;
})();
if(inst_58875){
var statearr_58940_59008 = state_58930__$1;
(statearr_58940_59008[(1)] = (5));

} else {
var statearr_58941_59009 = state_58930__$1;
(statearr_58941_59009[(1)] = (6));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_58931 === (15))){
var inst_58896 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.bridge.remote.log_messages_QMARK_) : cljs.core.deref.call(null,org.numenta.sanity.bridge.remote.log_messages_QMARK_));
var state_58930__$1 = state_58930;
if(cljs.core.truth_(inst_58896)){
var statearr_58942_59010 = state_58930__$1;
(statearr_58942_59010[(1)] = (17));

} else {
var statearr_58943_59011 = state_58930__$1;
(statearr_58943_59011[(1)] = (18));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_58931 === (21))){
var inst_58901 = (state_58930[(8)]);
var state_58930__$1 = state_58930;
var statearr_58944_59012 = state_58930__$1;
(statearr_58944_59012[(2)] = inst_58901);

(statearr_58944_59012[(1)] = (22));


return cljs.core.cst$kw$recur;
} else {
if((state_val_58931 === (13))){
var inst_58887 = (state_58930[(2)]);
var state_58930__$1 = state_58930;
var statearr_58945_59013 = state_58930__$1;
(statearr_58945_59013[(2)] = inst_58887);

(statearr_58945_59013[(1)] = (10));


return cljs.core.cst$kw$recur;
} else {
if((state_val_58931 === (22))){
var inst_58907 = (state_58930[(2)]);
var inst_58908 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.bridge.remote.log_raw_messages_QMARK_) : cljs.core.deref.call(null,org.numenta.sanity.bridge.remote.log_raw_messages_QMARK_));
var state_58930__$1 = (function (){var statearr_58946 = state_58930;
(statearr_58946[(9)] = inst_58907);

return statearr_58946;
})();
if(cljs.core.truth_(inst_58908)){
var statearr_58947_59014 = state_58930__$1;
(statearr_58947_59014[(1)] = (23));

} else {
var statearr_58948_59015 = state_58930__$1;
(statearr_58948_59015[(1)] = (24));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_58931 === (6))){
var inst_58874 = (state_58930[(10)]);
var inst_58878 = cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(inst_58874,to_network_c);
var state_58930__$1 = state_58930;
if(inst_58878){
var statearr_58949_59016 = state_58930__$1;
(statearr_58949_59016[(1)] = (8));

} else {
var statearr_58950_59017 = state_58930__$1;
(statearr_58950_59017[(1)] = (9));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_58931 === (28))){
var inst_58913 = (state_58930[(13)]);
var inst_58922 = (state_58930[(2)]);
var inst_58923 = ws.send(inst_58913);
var state_58930__$1 = (function (){var statearr_58951 = state_58930;
(statearr_58951[(14)] = inst_58923);

(statearr_58951[(15)] = inst_58922);

return statearr_58951;
})();
var statearr_58952_59018 = state_58930__$1;
(statearr_58952_59018[(2)] = null);

(statearr_58952_59018[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_58931 === (25))){
var inst_58914 = (state_58930[(16)]);
var inst_58913 = (state_58930[(13)]);
var inst_58913__$1 = (state_58930[(2)]);
var inst_58914__$1 = cljs.core.count(inst_58913__$1);
var inst_58915 = (inst_58914__$1 > org.numenta.sanity.bridge.remote.max_message_size);
var state_58930__$1 = (function (){var statearr_58953 = state_58930;
(statearr_58953[(16)] = inst_58914__$1);

(statearr_58953[(13)] = inst_58913__$1);

return statearr_58953;
})();
if(cljs.core.truth_(inst_58915)){
var statearr_58954_59019 = state_58930__$1;
(statearr_58954_59019[(1)] = (26));

} else {
var statearr_58955_59020 = state_58930__$1;
(statearr_58955_59020[(1)] = (27));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_58931 === (17))){
var inst_58891 = (state_58930[(7)]);
var inst_58898 = org.numenta.sanity.bridge.remote.log(inst_58891,"SENDING:");
var state_58930__$1 = state_58930;
var statearr_58956_59021 = state_58930__$1;
(statearr_58956_59021[(2)] = inst_58898);

(statearr_58956_59021[(1)] = (19));


return cljs.core.cst$kw$recur;
} else {
if((state_val_58931 === (3))){
var inst_58928 = (state_58930[(2)]);
var state_58930__$1 = state_58930;
return cljs.core.async.impl.ioc_helpers.return_chan(state_58930__$1,inst_58928);
} else {
if((state_val_58931 === (12))){
var state_58930__$1 = state_58930;
var statearr_58957_59022 = state_58930__$1;
(statearr_58957_59022[(2)] = null);

(statearr_58957_59022[(1)] = (13));


return cljs.core.cst$kw$recur;
} else {
if((state_val_58931 === (2))){
var inst_58868 = cljs.core.PersistentVector.EMPTY_NODE;
var inst_58869 = [teardown_c,to_network_c];
var inst_58870 = (new cljs.core.PersistentVector(null,2,(5),inst_58868,inst_58869,null));
var state_58930__$1 = state_58930;
return cljs.core.async.ioc_alts_BANG_.cljs$core$IFn$_invoke$arity$variadic(state_58930__$1,(4),inst_58870,cljs.core.array_seq([cljs.core.cst$kw$priority,true], 0));
} else {
if((state_val_58931 === (23))){
var inst_58907 = (state_58930[(9)]);
var inst_58910 = org.numenta.sanity.bridge.remote.log(inst_58907,"SENDING TEXT:");
var state_58930__$1 = state_58930;
var statearr_58958_59023 = state_58930__$1;
(statearr_58958_59023[(2)] = inst_58910);

(statearr_58958_59023[(1)] = (25));


return cljs.core.cst$kw$recur;
} else {
if((state_val_58931 === (19))){
var inst_58901 = (state_58930[(2)]);
var state_58930__$1 = (function (){var statearr_58959 = state_58930;
(statearr_58959[(8)] = inst_58901);

return statearr_58959;
})();
var statearr_58960_59024 = state_58930__$1;
(statearr_58960_59024[(1)] = (20));



return cljs.core.cst$kw$recur;
} else {
if((state_val_58931 === (11))){
var inst_58873 = (state_58930[(12)]);
var state_58930__$1 = state_58930;
var statearr_58962_59025 = state_58930__$1;
(statearr_58962_59025[(2)] = inst_58873);

(statearr_58962_59025[(1)] = (13));


return cljs.core.cst$kw$recur;
} else {
if((state_val_58931 === (9))){
var inst_58874 = (state_58930[(10)]);
var inst_58883 = cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(inst_58874,cljs.core.cst$kw$default);
var state_58930__$1 = state_58930;
if(inst_58883){
var statearr_58963_59026 = state_58930__$1;
(statearr_58963_59026[(1)] = (11));

} else {
var statearr_58964_59027 = state_58930__$1;
(statearr_58964_59027[(1)] = (12));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_58931 === (5))){
var state_58930__$1 = state_58930;
var statearr_58965_59028 = state_58930__$1;
(statearr_58965_59028[(2)] = null);

(statearr_58965_59028[(1)] = (7));


return cljs.core.cst$kw$recur;
} else {
if((state_val_58931 === (14))){
var state_58930__$1 = state_58930;
var statearr_58966_59029 = state_58930__$1;
(statearr_58966_59029[(2)] = null);

(statearr_58966_59029[(1)] = (16));


return cljs.core.cst$kw$recur;
} else {
if((state_val_58931 === (26))){
var inst_58914 = (state_58930[(16)]);
var inst_58913 = (state_58930[(13)]);
var inst_58917 = [cljs.core.str("Message too large! Size: "),cljs.core.str(inst_58914),cljs.core.str("Max-size: "),cljs.core.str(org.numenta.sanity.bridge.remote.max_message_size)].join('');
var inst_58918 = alert(inst_58917);
var inst_58919 = cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["Message too large!",inst_58913], 0));
var state_58930__$1 = (function (){var statearr_58967 = state_58930;
(statearr_58967[(17)] = inst_58918);

return statearr_58967;
})();
var statearr_58968_59030 = state_58930__$1;
(statearr_58968_59030[(2)] = inst_58919);

(statearr_58968_59030[(1)] = (28));


return cljs.core.cst$kw$recur;
} else {
if((state_val_58931 === (16))){
var inst_58926 = (state_58930[(2)]);
var state_58930__$1 = state_58930;
var statearr_58969_59031 = state_58930__$1;
(statearr_58969_59031[(2)] = inst_58926);

(statearr_58969_59031[(1)] = (3));


return cljs.core.cst$kw$recur;
} else {
if((state_val_58931 === (10))){
var inst_58889 = (state_58930[(2)]);
var state_58930__$1 = state_58930;
var statearr_58970_59032 = state_58930__$1;
(statearr_58970_59032[(2)] = inst_58889);

(statearr_58970_59032[(1)] = (7));


return cljs.core.cst$kw$recur;
} else {
if((state_val_58931 === (18))){
var inst_58891 = (state_58930[(7)]);
var state_58930__$1 = state_58930;
var statearr_58971_59033 = state_58930__$1;
(statearr_58971_59033[(2)] = inst_58891);

(statearr_58971_59033[(1)] = (19));


return cljs.core.cst$kw$recur;
} else {
if((state_val_58931 === (8))){
var inst_58872 = (state_58930[(11)]);
var inst_58881 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(inst_58872,(0),null);
var state_58930__$1 = state_58930;
var statearr_58972_59034 = state_58930__$1;
(statearr_58972_59034[(2)] = inst_58881);

(statearr_58972_59034[(1)] = (10));


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
}
}
});})(c__38109__auto__,G__58801,ws,teardown_c,connection_id_STAR_,local_resources,remote_resources))
;
return ((function (switch__37995__auto__,c__38109__auto__,G__58801,ws,teardown_c,connection_id_STAR_,local_resources,remote_resources){
return (function() {
var org$numenta$sanity$bridge$remote$connect_BANG__$_state_machine__37996__auto__ = null;
var org$numenta$sanity$bridge$remote$connect_BANG__$_state_machine__37996__auto____0 = (function (){
var statearr_58976 = [null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null];
(statearr_58976[(0)] = org$numenta$sanity$bridge$remote$connect_BANG__$_state_machine__37996__auto__);

(statearr_58976[(1)] = (1));

return statearr_58976;
});
var org$numenta$sanity$bridge$remote$connect_BANG__$_state_machine__37996__auto____1 = (function (state_58930){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_58930);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e58977){if((e58977 instanceof Object)){
var ex__37999__auto__ = e58977;
var statearr_58978_59035 = state_58930;
(statearr_58978_59035[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_58930);

return cljs.core.cst$kw$recur;
} else {
throw e58977;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__59036 = state_58930;
state_58930 = G__59036;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$bridge$remote$connect_BANG__$_state_machine__37996__auto__ = function(state_58930){
switch(arguments.length){
case 0:
return org$numenta$sanity$bridge$remote$connect_BANG__$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$bridge$remote$connect_BANG__$_state_machine__37996__auto____1.call(this,state_58930);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$bridge$remote$connect_BANG__$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$bridge$remote$connect_BANG__$_state_machine__37996__auto____0;
org$numenta$sanity$bridge$remote$connect_BANG__$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$bridge$remote$connect_BANG__$_state_machine__37996__auto____1;
return org$numenta$sanity$bridge$remote$connect_BANG__$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto__,G__58801,ws,teardown_c,connection_id_STAR_,local_resources,remote_resources))
})();
var state__38111__auto__ = (function (){var statearr_58979 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_58979[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto__);

return statearr_58979;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto__,G__58801,ws,teardown_c,connection_id_STAR_,local_resources,remote_resources))
);

return c__38109__auto__;
});})(G__58801,ws,teardown_c,connection_id_STAR_,local_resources,remote_resources))
);

(G__58801["onerror"] = ((function (G__58801,ws,teardown_c,connection_id_STAR_,local_resources,remote_resources){
return (function (evt){
cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["WebSocket error:"], 0));

return console.error(evt);
});})(G__58801,ws,teardown_c,connection_id_STAR_,local_resources,remote_resources))
);

(G__58801["onclose"] = ((function (G__58801,ws,teardown_c,connection_id_STAR_,local_resources,remote_resources){
return (function (evt){
(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(connection_id,null) : cljs.core.reset_BANG_.call(null,connection_id,null));

(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(connecting_QMARK_,false) : cljs.core.reset_BANG_.call(null,connecting_QMARK_,false));

cljs.core.async.close_BANG_(teardown_c);

return cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["WebSocket closed."], 0));
});})(G__58801,ws,teardown_c,connection_id_STAR_,local_resources,remote_resources))
);

(G__58801["onmessage"] = ((function (G__58801,ws,teardown_c,connection_id_STAR_,local_resources,remote_resources){
return (function (evt){
var vec__58980 = (function (){var G__58982 = evt.data;
var G__58982__$1 = (cljs.core.truth_((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.bridge.remote.log_raw_messages_QMARK_) : cljs.core.deref.call(null,org.numenta.sanity.bridge.remote.log_raw_messages_QMARK_)))?org.numenta.sanity.bridge.remote.log(G__58982,"RECEIVED TEXT:"):G__58982);
var G__58982__$2 = org.numenta.sanity.bridge.remote.read_transit_str(G__58982__$1,org.numenta.sanity.bridge.marshalling.read_handlers(target__GT_mchannel,((function (G__58982,G__58982__$1,G__58801,ws,teardown_c,connection_id_STAR_,local_resources,remote_resources){
return (function (t,v){
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(to_network_c,org.numenta.sanity.bridge.remote.target_put(t,v));
});})(G__58982,G__58982__$1,G__58801,ws,teardown_c,connection_id_STAR_,local_resources,remote_resources))
,((function (G__58982,G__58982__$1,G__58801,ws,teardown_c,connection_id_STAR_,local_resources,remote_resources){
return (function (t){
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(to_network_c,org.numenta.sanity.bridge.remote.target_close(t));
});})(G__58982,G__58982__$1,G__58801,ws,teardown_c,connection_id_STAR_,local_resources,remote_resources))
,remote_resources))
;
if(cljs.core.truth_((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.bridge.remote.log_messages_QMARK_) : cljs.core.deref.call(null,org.numenta.sanity.bridge.remote.log_messages_QMARK_)))){
return org.numenta.sanity.bridge.remote.log(G__58982__$2,"RECEIVED:");
} else {
return G__58982__$2;
}
})();
var op = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__58980,(0),null);
var target = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__58980,(1),null);
var msg = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__58980,(2),null);
var map__58981 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(target__GT_mchannel) : cljs.core.deref.call(null,target__GT_mchannel)).call(null,target);
var map__58981__$1 = ((((!((map__58981 == null)))?((((map__58981.cljs$lang$protocol_mask$partition0$ & (64))) || (map__58981.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__58981):map__58981);
var mchannel = map__58981__$1;
var ch = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__58981__$1,cljs.core.cst$kw$ch);
var single_use_QMARK_ = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__58981__$1,cljs.core.cst$kw$single_DASH_use_QMARK_);
if(cljs.core.truth_(ch)){
if(cljs.core.truth_(single_use_QMARK_)){
org.numenta.sanity.bridge.marshalling.release_BANG_(mchannel);
} else {
}

var G__58984 = op;
switch (G__58984) {
case "put!":
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(ch,msg);

break;
case "close!":
return cljs.core.async.close_BANG_(ch);

break;
default:
throw (new Error([cljs.core.str("No matching clause: "),cljs.core.str(op)].join('')));

}
} else {
cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["UNRECOGNIZED TARGET",target], 0));

return cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["Known targets:",(cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(target__GT_mchannel) : cljs.core.deref.call(null,target__GT_mchannel))], 0));
}
});})(G__58801,ws,teardown_c,connection_id_STAR_,local_resources,remote_resources))
);

return G__58801;
});
org.numenta.sanity.bridge.remote.init = (function org$numenta$sanity$bridge$remote$init(ws_url){
var to_network_c = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1(cljs.core.async.sliding_buffer((1024)));
var connection_id = (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(null) : cljs.core.atom.call(null,null));
var on_connect_c = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1(cljs.core.async.sliding_buffer((1024)));
var connecting_QMARK_ = (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(false) : cljs.core.atom.call(null,false));
var target__GT_mchannel = (function (){var G__59211 = cljs.core.PersistentArrayMap.EMPTY;
return (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(G__59211) : cljs.core.atom.call(null,G__59211));
})();
return ((function (to_network_c,connection_id,on_connect_c,connecting_QMARK_,target__GT_mchannel){
return (function org$numenta$sanity$bridge$remote$init_$_pipe_to_remote_target(t,ch){
var last_seen_connection_id = (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(null) : cljs.core.atom.call(null,null));
var reconnect_blob = (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(null) : cljs.core.atom.call(null,null));
var blob_resets_c = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
var blob_resets_cproxy = org.numenta.sanity.bridge.marshalling.channel.cljs$core$IFn$_invoke$arity$1(blob_resets_c);
var c__38109__auto___59384 = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto___59384,last_seen_connection_id,reconnect_blob,blob_resets_c,blob_resets_cproxy,to_network_c,connection_id,on_connect_c,connecting_QMARK_,target__GT_mchannel){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto___59384,last_seen_connection_id,reconnect_blob,blob_resets_c,blob_resets_cproxy,to_network_c,connection_id,on_connect_c,connecting_QMARK_,target__GT_mchannel){
return (function (state_59311){
var state_val_59312 = (state_59311[(1)]);
if((state_val_59312 === (1))){
var state_59311__$1 = state_59311;
var statearr_59313_59385 = state_59311__$1;
(statearr_59313_59385[(2)] = null);

(statearr_59313_59385[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_59312 === (2))){
var state_59311__$1 = state_59311;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_59311__$1,(4),blob_resets_c);
} else {
if((state_val_59312 === (3))){
var inst_59309 = (state_59311[(2)]);
var state_59311__$1 = state_59311;
return cljs.core.async.impl.ioc_helpers.return_chan(state_59311__$1,inst_59309);
} else {
if((state_val_59312 === (4))){
var inst_59300 = (state_59311[(7)]);
var inst_59300__$1 = (state_59311[(2)]);
var inst_59301 = (inst_59300__$1 == null);
var state_59311__$1 = (function (){var statearr_59314 = state_59311;
(statearr_59314[(7)] = inst_59300__$1);

return statearr_59314;
})();
if(cljs.core.truth_(inst_59301)){
var statearr_59315_59386 = state_59311__$1;
(statearr_59315_59386[(1)] = (5));

} else {
var statearr_59316_59387 = state_59311__$1;
(statearr_59316_59387[(1)] = (6));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_59312 === (5))){
var state_59311__$1 = state_59311;
var statearr_59317_59388 = state_59311__$1;
(statearr_59317_59388[(2)] = null);

(statearr_59317_59388[(1)] = (7));


return cljs.core.cst$kw$recur;
} else {
if((state_val_59312 === (6))){
var inst_59300 = (state_59311[(7)]);
var inst_59304 = (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(reconnect_blob,inst_59300) : cljs.core.reset_BANG_.call(null,reconnect_blob,inst_59300));
var state_59311__$1 = (function (){var statearr_59318 = state_59311;
(statearr_59318[(8)] = inst_59304);

return statearr_59318;
})();
var statearr_59319_59389 = state_59311__$1;
(statearr_59319_59389[(2)] = null);

(statearr_59319_59389[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_59312 === (7))){
var inst_59307 = (state_59311[(2)]);
var state_59311__$1 = state_59311;
var statearr_59320_59390 = state_59311__$1;
(statearr_59320_59390[(2)] = inst_59307);

(statearr_59320_59390[(1)] = (3));


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
});})(c__38109__auto___59384,last_seen_connection_id,reconnect_blob,blob_resets_c,blob_resets_cproxy,to_network_c,connection_id,on_connect_c,connecting_QMARK_,target__GT_mchannel))
;
return ((function (switch__37995__auto__,c__38109__auto___59384,last_seen_connection_id,reconnect_blob,blob_resets_c,blob_resets_cproxy,to_network_c,connection_id,on_connect_c,connecting_QMARK_,target__GT_mchannel){
return (function() {
var org$numenta$sanity$bridge$remote$init_$_pipe_to_remote_target_$_state_machine__37996__auto__ = null;
var org$numenta$sanity$bridge$remote$init_$_pipe_to_remote_target_$_state_machine__37996__auto____0 = (function (){
var statearr_59324 = [null,null,null,null,null,null,null,null,null];
(statearr_59324[(0)] = org$numenta$sanity$bridge$remote$init_$_pipe_to_remote_target_$_state_machine__37996__auto__);

(statearr_59324[(1)] = (1));

return statearr_59324;
});
var org$numenta$sanity$bridge$remote$init_$_pipe_to_remote_target_$_state_machine__37996__auto____1 = (function (state_59311){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_59311);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e59325){if((e59325 instanceof Object)){
var ex__37999__auto__ = e59325;
var statearr_59326_59391 = state_59311;
(statearr_59326_59391[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_59311);

return cljs.core.cst$kw$recur;
} else {
throw e59325;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__59392 = state_59311;
state_59311 = G__59392;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$bridge$remote$init_$_pipe_to_remote_target_$_state_machine__37996__auto__ = function(state_59311){
switch(arguments.length){
case 0:
return org$numenta$sanity$bridge$remote$init_$_pipe_to_remote_target_$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$bridge$remote$init_$_pipe_to_remote_target_$_state_machine__37996__auto____1.call(this,state_59311);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$bridge$remote$init_$_pipe_to_remote_target_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$bridge$remote$init_$_pipe_to_remote_target_$_state_machine__37996__auto____0;
org$numenta$sanity$bridge$remote$init_$_pipe_to_remote_target_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$bridge$remote$init_$_pipe_to_remote_target_$_state_machine__37996__auto____1;
return org$numenta$sanity$bridge$remote$init_$_pipe_to_remote_target_$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto___59384,last_seen_connection_id,reconnect_blob,blob_resets_c,blob_resets_cproxy,to_network_c,connection_id,on_connect_c,connecting_QMARK_,target__GT_mchannel))
})();
var state__38111__auto__ = (function (){var statearr_59327 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_59327[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto___59384);

return statearr_59327;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto___59384,last_seen_connection_id,reconnect_blob,blob_resets_c,blob_resets_cproxy,to_network_c,connection_id,on_connect_c,connecting_QMARK_,target__GT_mchannel))
);


var c__38109__auto__ = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto__,last_seen_connection_id,reconnect_blob,blob_resets_c,blob_resets_cproxy,to_network_c,connection_id,on_connect_c,connecting_QMARK_,target__GT_mchannel){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto__,last_seen_connection_id,reconnect_blob,blob_resets_c,blob_resets_cproxy,to_network_c,connection_id,on_connect_c,connecting_QMARK_,target__GT_mchannel){
return (function (state_59355){
var state_val_59356 = (state_59355[(1)]);
if((state_val_59356 === (7))){
var inst_59330 = (state_59355[(7)]);
var inst_59345 = (state_59355[(2)]);
var inst_59346 = (inst_59330 == null);
var state_59355__$1 = (function (){var statearr_59357 = state_59355;
(statearr_59357[(8)] = inst_59345);

return statearr_59357;
})();
if(cljs.core.truth_(inst_59346)){
var statearr_59358_59393 = state_59355__$1;
(statearr_59358_59393[(1)] = (11));

} else {
var statearr_59359_59394 = state_59355__$1;
(statearr_59359_59394[(1)] = (12));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_59356 === (1))){
var state_59355__$1 = state_59355;
var statearr_59360_59395 = state_59355__$1;
(statearr_59360_59395[(2)] = null);

(statearr_59360_59395[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_59356 === (4))){
var inst_59330 = (state_59355[(7)]);
var inst_59330__$1 = (state_59355[(2)]);
var inst_59331 = (function (){var v = inst_59330__$1;
return ((function (v,inst_59330,inst_59330__$1,state_val_59356,c__38109__auto__,last_seen_connection_id,reconnect_blob,blob_resets_c,blob_resets_cproxy,to_network_c,connection_id,on_connect_c,connecting_QMARK_,target__GT_mchannel){
return (function (){
if((((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(last_seen_connection_id) : cljs.core.deref.call(null,last_seen_connection_id)) == null)) || (cljs.core.not_EQ_.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(connection_id) : cljs.core.deref.call(null,connection_id)),(cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(last_seen_connection_id) : cljs.core.deref.call(null,last_seen_connection_id))))){
cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(to_network_c,org.numenta.sanity.bridge.remote.target_put(t,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, ["connect",(cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(reconnect_blob) : cljs.core.deref.call(null,reconnect_blob)),blob_resets_cproxy], null)));

var G__59361_59396 = last_seen_connection_id;
var G__59362_59397 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(connection_id) : cljs.core.deref.call(null,connection_id));
(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__59361_59396,G__59362_59397) : cljs.core.reset_BANG_.call(null,G__59361_59396,G__59362_59397));
} else {
}

if(!((v == null))){
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(to_network_c,org.numenta.sanity.bridge.remote.target_put(t,v));
} else {
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(to_network_c,org.numenta.sanity.bridge.remote.target_close(t));
}
});
;})(v,inst_59330,inst_59330__$1,state_val_59356,c__38109__auto__,last_seen_connection_id,reconnect_blob,blob_resets_c,blob_resets_cproxy,to_network_c,connection_id,on_connect_c,connecting_QMARK_,target__GT_mchannel))
})();
var inst_59332 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(connection_id) : cljs.core.deref.call(null,connection_id));
var state_59355__$1 = (function (){var statearr_59363 = state_59355;
(statearr_59363[(7)] = inst_59330__$1);

(statearr_59363[(9)] = inst_59331);

return statearr_59363;
})();
if(cljs.core.truth_(inst_59332)){
var statearr_59364_59398 = state_59355__$1;
(statearr_59364_59398[(1)] = (5));

} else {
var statearr_59365_59399 = state_59355__$1;
(statearr_59365_59399[(1)] = (6));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_59356 === (13))){
var inst_59351 = (state_59355[(2)]);
var state_59355__$1 = state_59355;
var statearr_59366_59400 = state_59355__$1;
(statearr_59366_59400[(2)] = inst_59351);

(statearr_59366_59400[(1)] = (3));


return cljs.core.cst$kw$recur;
} else {
if((state_val_59356 === (6))){
var inst_59331 = (state_59355[(9)]);
var inst_59336 = cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(on_connect_c,inst_59331);
var inst_59337 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(connecting_QMARK_) : cljs.core.deref.call(null,connecting_QMARK_));
var state_59355__$1 = (function (){var statearr_59367 = state_59355;
(statearr_59367[(10)] = inst_59336);

return statearr_59367;
})();
if(cljs.core.truth_(inst_59337)){
var statearr_59368_59401 = state_59355__$1;
(statearr_59368_59401[(1)] = (8));

} else {
var statearr_59369_59402 = state_59355__$1;
(statearr_59369_59402[(1)] = (9));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_59356 === (3))){
var inst_59353 = (state_59355[(2)]);
var state_59355__$1 = state_59355;
return cljs.core.async.impl.ioc_helpers.return_chan(state_59355__$1,inst_59353);
} else {
if((state_val_59356 === (12))){
var state_59355__$1 = state_59355;
var statearr_59370_59403 = state_59355__$1;
(statearr_59370_59403[(2)] = null);

(statearr_59370_59403[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_59356 === (2))){
var state_59355__$1 = state_59355;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_59355__$1,(4),ch);
} else {
if((state_val_59356 === (11))){
var state_59355__$1 = state_59355;
var statearr_59371_59404 = state_59355__$1;
(statearr_59371_59404[(2)] = null);

(statearr_59371_59404[(1)] = (13));


return cljs.core.cst$kw$recur;
} else {
if((state_val_59356 === (9))){
var inst_59340 = (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(connecting_QMARK_,true) : cljs.core.reset_BANG_.call(null,connecting_QMARK_,true));
var inst_59341 = org.numenta.sanity.bridge.remote.connect_BANG_(connection_id,to_network_c,on_connect_c,ws_url,connecting_QMARK_,target__GT_mchannel);
var state_59355__$1 = (function (){var statearr_59372 = state_59355;
(statearr_59372[(11)] = inst_59340);

return statearr_59372;
})();
var statearr_59373_59405 = state_59355__$1;
(statearr_59373_59405[(2)] = inst_59341);

(statearr_59373_59405[(1)] = (10));


return cljs.core.cst$kw$recur;
} else {
if((state_val_59356 === (5))){
var inst_59331 = (state_59355[(9)]);
var inst_59334 = (inst_59331.cljs$core$IFn$_invoke$arity$0 ? inst_59331.cljs$core$IFn$_invoke$arity$0() : inst_59331.call(null));
var state_59355__$1 = state_59355;
var statearr_59374_59406 = state_59355__$1;
(statearr_59374_59406[(2)] = inst_59334);

(statearr_59374_59406[(1)] = (7));


return cljs.core.cst$kw$recur;
} else {
if((state_val_59356 === (10))){
var inst_59343 = (state_59355[(2)]);
var state_59355__$1 = state_59355;
var statearr_59375_59407 = state_59355__$1;
(statearr_59375_59407[(2)] = inst_59343);

(statearr_59375_59407[(1)] = (7));


return cljs.core.cst$kw$recur;
} else {
if((state_val_59356 === (8))){
var state_59355__$1 = state_59355;
var statearr_59376_59408 = state_59355__$1;
(statearr_59376_59408[(2)] = null);

(statearr_59376_59408[(1)] = (10));


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
});})(c__38109__auto__,last_seen_connection_id,reconnect_blob,blob_resets_c,blob_resets_cproxy,to_network_c,connection_id,on_connect_c,connecting_QMARK_,target__GT_mchannel))
;
return ((function (switch__37995__auto__,c__38109__auto__,last_seen_connection_id,reconnect_blob,blob_resets_c,blob_resets_cproxy,to_network_c,connection_id,on_connect_c,connecting_QMARK_,target__GT_mchannel){
return (function() {
var org$numenta$sanity$bridge$remote$init_$_pipe_to_remote_target_$_state_machine__37996__auto__ = null;
var org$numenta$sanity$bridge$remote$init_$_pipe_to_remote_target_$_state_machine__37996__auto____0 = (function (){
var statearr_59380 = [null,null,null,null,null,null,null,null,null,null,null,null];
(statearr_59380[(0)] = org$numenta$sanity$bridge$remote$init_$_pipe_to_remote_target_$_state_machine__37996__auto__);

(statearr_59380[(1)] = (1));

return statearr_59380;
});
var org$numenta$sanity$bridge$remote$init_$_pipe_to_remote_target_$_state_machine__37996__auto____1 = (function (state_59355){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_59355);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e59381){if((e59381 instanceof Object)){
var ex__37999__auto__ = e59381;
var statearr_59382_59409 = state_59355;
(statearr_59382_59409[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_59355);

return cljs.core.cst$kw$recur;
} else {
throw e59381;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__59410 = state_59355;
state_59355 = G__59410;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$bridge$remote$init_$_pipe_to_remote_target_$_state_machine__37996__auto__ = function(state_59355){
switch(arguments.length){
case 0:
return org$numenta$sanity$bridge$remote$init_$_pipe_to_remote_target_$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$bridge$remote$init_$_pipe_to_remote_target_$_state_machine__37996__auto____1.call(this,state_59355);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$bridge$remote$init_$_pipe_to_remote_target_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$bridge$remote$init_$_pipe_to_remote_target_$_state_machine__37996__auto____0;
org$numenta$sanity$bridge$remote$init_$_pipe_to_remote_target_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$bridge$remote$init_$_pipe_to_remote_target_$_state_machine__37996__auto____1;
return org$numenta$sanity$bridge$remote$init_$_pipe_to_remote_target_$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto__,last_seen_connection_id,reconnect_blob,blob_resets_c,blob_resets_cproxy,to_network_c,connection_id,on_connect_c,connecting_QMARK_,target__GT_mchannel))
})();
var state__38111__auto__ = (function (){var statearr_59383 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_59383[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto__);

return statearr_59383;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto__,last_seen_connection_id,reconnect_blob,blob_resets_c,blob_resets_cproxy,to_network_c,connection_id,on_connect_c,connecting_QMARK_,target__GT_mchannel))
);

return c__38109__auto__;
});
;})(to_network_c,connection_id,on_connect_c,connecting_QMARK_,target__GT_mchannel))
});
(window["sanityLogMessages"] = (function (){
return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.bridge.remote.log_messages_QMARK_,cljs.core.not);
}));
(window["sanityLogRawMessages"] = (function (){
return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.bridge.remote.log_raw_messages_QMARK_,cljs.core.not);
}));
(window["sanityLogUgly"] = (function (){
return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.bridge.remote.log_pretty_QMARK_,cljs.core.not);
}));
var G__59411_59412 = [cljs.core.str("Call sanityLogMessages() or sanityLogRawMessages() to display websocket "),cljs.core.str("traffic. Call sanityLogUgly() to condense the output.")].join('');
console.log(G__59411_59412);
