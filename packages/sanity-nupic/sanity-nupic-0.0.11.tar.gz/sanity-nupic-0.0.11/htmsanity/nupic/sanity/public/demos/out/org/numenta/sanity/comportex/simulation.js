// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.numenta.sanity.comportex.simulation');
goog.require('cljs.core');
goog.require('org.nfrac.comportex.protocols');
goog.require('cljs.core.async');
goog.require('org.numenta.sanity.bridge.marshalling');
goog.require('org.nfrac.comportex.core');
goog.require('org.nfrac.comportex.util');
org.numenta.sanity.comportex.simulation.should_go_QMARK__BANG_ = (function org$numenta$sanity$comportex$simulation$should_go_QMARK__BANG_(options){
var map__68488 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(options) : cljs.core.deref.call(null,options));
var map__68488__$1 = ((((!((map__68488 == null)))?((((map__68488.cljs$lang$protocol_mask$partition0$ & (64))) || (map__68488.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__68488):map__68488);
var go_QMARK_ = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__68488__$1,cljs.core.cst$kw$go_QMARK_);
var force_n_steps = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__68488__$1,cljs.core.cst$kw$force_DASH_n_DASH_steps);
var step_ms = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__68488__$1,cljs.core.cst$kw$step_DASH_ms);
if(cljs.core.truth_(go_QMARK_)){
return step_ms;
} else {
if((force_n_steps > (0))){
cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(options,cljs.core.update,cljs.core.cst$kw$force_DASH_n_DASH_steps,cljs.core.dec);

return (0);
} else {
return false;

}
}
});
org.numenta.sanity.comportex.simulation.simulation_loop = (function org$numenta$sanity$comportex$simulation$simulation_loop(model,world,out,options,sim_closed_QMARK_,htm_step){
var c__38109__auto__ = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto__){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto__){
return (function (state_68589){
var state_val_68590 = (state_68589[(1)]);
if((state_val_68590 === (7))){
var state_68589__$1 = state_68589;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_68589__$1,(10),world);
} else {
if((state_val_68590 === (1))){
var state_68589__$1 = state_68589;
var statearr_68591_68620 = state_68589__$1;
(statearr_68591_68620[(2)] = null);

(statearr_68591_68620[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_68590 === (4))){
var inst_68559 = (state_68589[(7)]);
var inst_68559__$1 = org.numenta.sanity.comportex.simulation.should_go_QMARK__BANG_(options);
var state_68589__$1 = (function (){var statearr_68592 = state_68589;
(statearr_68592[(7)] = inst_68559__$1);

return statearr_68592;
})();
if(cljs.core.truth_(inst_68559__$1)){
var statearr_68593_68621 = state_68589__$1;
(statearr_68593_68621[(1)] = (7));

} else {
var statearr_68594_68622 = state_68589__$1;
(statearr_68594_68622[(1)] = (8));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_68590 === (15))){
var inst_68582 = (function (){return ((function (state_val_68590,c__38109__auto__){
return (function (_,___$1,___$2,___$3){
cljs.core.remove_watch(options,cljs.core.cst$kw$run_DASH_sim);

return org$numenta$sanity$comportex$simulation$simulation_loop(model,world,out,options,sim_closed_QMARK_,htm_step);
});
;})(state_val_68590,c__38109__auto__))
})();
var inst_68583 = cljs.core.add_watch(options,cljs.core.cst$kw$run_DASH_sim,inst_68582);
var state_68589__$1 = state_68589;
var statearr_68595_68623 = state_68589__$1;
(statearr_68595_68623[(2)] = inst_68583);

(statearr_68595_68623[(1)] = (17));


return cljs.core.cst$kw$recur;
} else {
if((state_val_68590 === (13))){
var inst_68572 = (state_68589[(2)]);
var state_68589__$1 = state_68589;
var statearr_68596_68624 = state_68589__$1;
(statearr_68596_68624[(2)] = inst_68572);

(statearr_68596_68624[(1)] = (9));


return cljs.core.cst$kw$recur;
} else {
if((state_val_68590 === (6))){
var inst_68578 = (state_68589[(2)]);
var state_68589__$1 = state_68589;
var statearr_68597_68625 = state_68589__$1;
(statearr_68597_68625[(2)] = inst_68578);

(statearr_68597_68625[(1)] = (3));


return cljs.core.cst$kw$recur;
} else {
if((state_val_68590 === (17))){
var inst_68587 = (state_68589[(2)]);
var state_68589__$1 = state_68589;
return cljs.core.async.impl.ioc_helpers.return_chan(state_68589__$1,inst_68587);
} else {
if((state_val_68590 === (3))){
var inst_68580 = (state_68589[(2)]);
var state_68589__$1 = state_68589;
if(cljs.core.truth_(inst_68580)){
var statearr_68598_68626 = state_68589__$1;
(statearr_68598_68626[(1)] = (15));

} else {
var statearr_68599_68627 = state_68589__$1;
(statearr_68599_68627[(1)] = (16));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_68590 === (12))){
var state_68589__$1 = state_68589;
var statearr_68600_68628 = state_68589__$1;
(statearr_68600_68628[(2)] = null);

(statearr_68600_68628[(1)] = (13));


return cljs.core.cst$kw$recur;
} else {
if((state_val_68590 === (2))){
var inst_68556 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(sim_closed_QMARK_) : cljs.core.deref.call(null,sim_closed_QMARK_));
var inst_68557 = cljs.core.not(inst_68556);
var state_68589__$1 = state_68589;
if(inst_68557){
var statearr_68601_68629 = state_68589__$1;
(statearr_68601_68629[(1)] = (4));

} else {
var statearr_68602_68630 = state_68589__$1;
(statearr_68602_68630[(1)] = (5));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_68590 === (11))){
var inst_68562 = (state_68589[(8)]);
var inst_68559 = (state_68589[(7)]);
var inst_68564 = cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$3(model,htm_step,inst_68562);
var inst_68565 = cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(out,inst_68564);
var inst_68566 = cljs.core.async.timeout(inst_68559);
var state_68589__$1 = (function (){var statearr_68603 = state_68589;
(statearr_68603[(9)] = inst_68565);

return statearr_68603;
})();
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_68589__$1,(14),inst_68566);
} else {
if((state_val_68590 === (9))){
var inst_68575 = (state_68589[(2)]);
var state_68589__$1 = state_68589;
var statearr_68604_68631 = state_68589__$1;
(statearr_68604_68631[(2)] = inst_68575);

(statearr_68604_68631[(1)] = (6));


return cljs.core.cst$kw$recur;
} else {
if((state_val_68590 === (5))){
var state_68589__$1 = state_68589;
var statearr_68605_68632 = state_68589__$1;
(statearr_68605_68632[(2)] = null);

(statearr_68605_68632[(1)] = (6));


return cljs.core.cst$kw$recur;
} else {
if((state_val_68590 === (14))){
var inst_68568 = (state_68589[(2)]);
var state_68589__$1 = (function (){var statearr_68606 = state_68589;
(statearr_68606[(10)] = inst_68568);

return statearr_68606;
})();
var statearr_68607_68633 = state_68589__$1;
(statearr_68607_68633[(2)] = null);

(statearr_68607_68633[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_68590 === (16))){
var inst_68585 = (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(sim_closed_QMARK_,true) : cljs.core.reset_BANG_.call(null,sim_closed_QMARK_,true));
var state_68589__$1 = state_68589;
var statearr_68608_68634 = state_68589__$1;
(statearr_68608_68634[(2)] = inst_68585);

(statearr_68608_68634[(1)] = (17));


return cljs.core.cst$kw$recur;
} else {
if((state_val_68590 === (10))){
var inst_68562 = (state_68589[(8)]);
var inst_68562__$1 = (state_68589[(2)]);
var state_68589__$1 = (function (){var statearr_68609 = state_68589;
(statearr_68609[(8)] = inst_68562__$1);

return statearr_68609;
})();
if(cljs.core.truth_(inst_68562__$1)){
var statearr_68610_68635 = state_68589__$1;
(statearr_68610_68635[(1)] = (11));

} else {
var statearr_68611_68636 = state_68589__$1;
(statearr_68611_68636[(1)] = (12));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_68590 === (8))){
var state_68589__$1 = state_68589;
var statearr_68612_68637 = state_68589__$1;
(statearr_68612_68637[(2)] = true);

(statearr_68612_68637[(1)] = (9));


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
});})(c__38109__auto__))
;
return ((function (switch__37995__auto__,c__38109__auto__){
return (function() {
var org$numenta$sanity$comportex$simulation$simulation_loop_$_state_machine__37996__auto__ = null;
var org$numenta$sanity$comportex$simulation$simulation_loop_$_state_machine__37996__auto____0 = (function (){
var statearr_68616 = [null,null,null,null,null,null,null,null,null,null,null];
(statearr_68616[(0)] = org$numenta$sanity$comportex$simulation$simulation_loop_$_state_machine__37996__auto__);

(statearr_68616[(1)] = (1));

return statearr_68616;
});
var org$numenta$sanity$comportex$simulation$simulation_loop_$_state_machine__37996__auto____1 = (function (state_68589){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_68589);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e68617){if((e68617 instanceof Object)){
var ex__37999__auto__ = e68617;
var statearr_68618_68638 = state_68589;
(statearr_68618_68638[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_68589);

return cljs.core.cst$kw$recur;
} else {
throw e68617;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__68639 = state_68589;
state_68589 = G__68639;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$comportex$simulation$simulation_loop_$_state_machine__37996__auto__ = function(state_68589){
switch(arguments.length){
case 0:
return org$numenta$sanity$comportex$simulation$simulation_loop_$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$comportex$simulation$simulation_loop_$_state_machine__37996__auto____1.call(this,state_68589);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$comportex$simulation$simulation_loop_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$comportex$simulation$simulation_loop_$_state_machine__37996__auto____0;
org$numenta$sanity$comportex$simulation$simulation_loop_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$comportex$simulation$simulation_loop_$_state_machine__37996__auto____1;
return org$numenta$sanity$comportex$simulation$simulation_loop_$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto__))
})();
var state__38111__auto__ = (function (){var statearr_68619 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_68619[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto__);

return statearr_68619;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto__))
);

return c__38109__auto__;
});
org.numenta.sanity.comportex.simulation.command_handler = (function org$numenta$sanity$comportex$simulation$command_handler(model,options,status,status_subscribers,client_infos,all_client_infos){
return (function org$numenta$sanity$comportex$simulation$command_handler_$_handle_command(c){
var vec__68685 = c;
var vec__68686 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__68685,(0),null);
var command = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__68686,(0),null);
var xs = cljs.core.nthnext(vec__68686,(1));
var client_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__68685,(1),null);
var client_info = (function (){var or__6153__auto__ = cljs.core.get.cljs$core$IFn$_invoke$arity$2((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(client_infos) : cljs.core.deref.call(null,client_infos)),client_id);
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
var v = (function (){var G__68687 = cljs.core.PersistentArrayMap.EMPTY;
return (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(G__68687) : cljs.core.atom.call(null,G__68687));
})();
cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(client_infos,cljs.core.assoc,client_id,v);

return v;
}
})();
var G__68688 = command;
switch (G__68688) {
case "client-disconnect":
cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["SIMULATION: Client disconnected."], 0));

return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$3(status_subscribers,cljs.core.disj,cljs.core.cst$kw$sim_DASH_status_DASH_subscriber.cljs$core$IFn$_invoke$arity$1((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(client_info) : cljs.core.deref.call(null,client_info))));

break;
case "connect":
var vec__68689 = xs;
var old_client_info = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__68689,(0),null);
var map__68690 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__68689,(1),null);
var map__68690__$1 = ((((!((map__68690 == null)))?((((map__68690.cljs$lang$protocol_mask$partition0$ & (64))) || (map__68690.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__68690):map__68690);
var subscriber_c = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__68690__$1,cljs.core.cst$kw$ch);
cljs.core.add_watch(client_info,cljs.core.cst$kw$org$numenta$sanity$comportex$simulation_SLASH_push_DASH_to_DASH_client,((function (vec__68689,old_client_info,map__68690,map__68690__$1,subscriber_c,G__68688,vec__68685,vec__68686,command,xs,client_id,client_info){
return (function (_,___$1,___$2,v){
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(subscriber_c,cljs.core.update.cljs$core$IFn$_invoke$arity$3(v,cljs.core.cst$kw$sim_DASH_status_DASH_subscriber,((function (vec__68689,old_client_info,map__68690,map__68690__$1,subscriber_c,G__68688,vec__68685,vec__68686,command,xs,client_id,client_info){
return (function (subscriber_mchannel){
return org.numenta.sanity.bridge.marshalling.channel_weak(cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(subscriber_mchannel,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$ch,cljs.core.cst$kw$target_DASH_id], null)));
});})(vec__68689,old_client_info,map__68690,map__68690__$1,subscriber_c,G__68688,vec__68685,vec__68686,command,xs,client_id,client_info))
));
});})(vec__68689,old_client_info,map__68690,map__68690__$1,subscriber_c,G__68688,vec__68685,vec__68686,command,xs,client_id,client_info))
);

var temp__4657__auto__ = cljs.core.cst$kw$sim_DASH_status_DASH_subscriber.cljs$core$IFn$_invoke$arity$1(old_client_info);
if(cljs.core.truth_(temp__4657__auto__)){
var map__68692 = temp__4657__auto__;
var map__68692__$1 = ((((!((map__68692 == null)))?((((map__68692.cljs$lang$protocol_mask$partition0$ & (64))) || (map__68692.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__68692):map__68692);
var subscriber_c__$1 = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__68692__$1,cljs.core.cst$kw$ch);
cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["SIMULATION: Client resubscribed to status."], 0));

cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$3(status_subscribers,cljs.core.conj,subscriber_c__$1);

return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(client_info,cljs.core.assoc,cljs.core.cst$kw$sim_DASH_status_DASH_subscriber,subscriber_c__$1);
} else {
return null;
}

break;
case "step":
return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(options,cljs.core.update,cljs.core.cst$kw$force_DASH_n_DASH_steps,cljs.core.inc);

break;
case "set-spec":
var vec__68694 = xs;
var path = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__68694,(0),null);
var v = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__68694,(1),null);
return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(model,cljs.core.assoc_in,path,v);

break;
case "restart":
var vec__68695 = xs;
var map__68696 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__68695,(0),null);
var map__68696__$1 = ((((!((map__68696 == null)))?((((map__68696.cljs$lang$protocol_mask$partition0$ & (64))) || (map__68696.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__68696):map__68696);
var response_c = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__68696__$1,cljs.core.cst$kw$ch);
cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$2(model,org.nfrac.comportex.protocols.restart);

return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(response_c,cljs.core.cst$kw$done);

break;
case "toggle":
return cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["SIMULATION TOGGLE. Current timestep:",org.nfrac.comportex.protocols.timestep((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(model) : cljs.core.deref.call(null,model))),cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(options,cljs.core.update,cljs.core.cst$kw$go_QMARK_,cljs.core.not)], 0));

break;
case "pause":
cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["SIMULATION PAUSE. Current timestep:",org.nfrac.comportex.protocols.timestep((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(model) : cljs.core.deref.call(null,model)))], 0));

return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(options,cljs.core.assoc,cljs.core.cst$kw$go_QMARK_,false);

break;
case "run":
cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["SIMULATION RUN. Current timestep:",org.nfrac.comportex.protocols.timestep((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(model) : cljs.core.deref.call(null,model)))], 0));

return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(options,cljs.core.assoc,cljs.core.cst$kw$go_QMARK_,true);

break;
case "set-step-ms":
var vec__68698 = xs;
var t = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__68698,(0),null);
return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(options,cljs.core.assoc,cljs.core.cst$kw$step_DASH_ms,t);

break;
case "subscribe-to-status":
var vec__68699 = xs;
var subscriber_mchannel = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__68699,(0),null);
var subscriber_c = cljs.core.cst$kw$ch.cljs$core$IFn$_invoke$arity$1(subscriber_mchannel);
cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["SIMULATION: Client subscribed to status."], 0));

cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$3(status_subscribers,cljs.core.conj,subscriber_c);

cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(client_info,cljs.core.assoc,cljs.core.cst$kw$sim_DASH_status_DASH_subscriber,subscriber_mchannel);

return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(subscriber_c,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(status) : cljs.core.deref.call(null,status))], null));

break;
default:
throw (new Error([cljs.core.str("No matching clause: "),cljs.core.str(command)].join('')));

}
});
});
org.numenta.sanity.comportex.simulation.handle_commands = (function org$numenta$sanity$comportex$simulation$handle_commands(commands,model,options,sim_closed_QMARK_){
var status = (function (){var G__68753 = cljs.core.cst$kw$go_QMARK_.cljs$core$IFn$_invoke$arity$1((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(options) : cljs.core.deref.call(null,options)));
return (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(G__68753) : cljs.core.atom.call(null,G__68753));
})();
var status_subscribers = (function (){var G__68754 = cljs.core.PersistentHashSet.EMPTY;
return (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(G__68754) : cljs.core.atom.call(null,G__68754));
})();
var client_infos = (function (){var G__68755 = cljs.core.PersistentArrayMap.EMPTY;
return (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(G__68755) : cljs.core.atom.call(null,G__68755));
})();
var all_client_infos = (function (){var G__68756 = cljs.core.PersistentHashSet.EMPTY;
return (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(G__68756) : cljs.core.atom.call(null,G__68756));
})();
var handle_command = org.numenta.sanity.comportex.simulation.command_handler(model,options,status,status_subscribers,client_infos,all_client_infos);
cljs.core.add_watch(options,cljs.core.cst$kw$org$numenta$sanity$comportex$simulation_SLASH_extract_DASH_status_DASH_change,((function (status,status_subscribers,client_infos,all_client_infos,handle_command){
return (function (_,___$1,oldv,newv){
var map__68757 = newv;
var map__68757__$1 = ((((!((map__68757 == null)))?((((map__68757.cljs$lang$protocol_mask$partition0$ & (64))) || (map__68757.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__68757):map__68757);
var go_QMARK_ = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__68757__$1,cljs.core.cst$kw$go_QMARK_);
if(cljs.core.not_EQ_.cljs$core$IFn$_invoke$arity$2(go_QMARK_,cljs.core.cst$kw$go_QMARK_.cljs$core$IFn$_invoke$arity$1(oldv))){
return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(status,go_QMARK_) : cljs.core.reset_BANG_.call(null,status,go_QMARK_));
} else {
return null;
}
});})(status,status_subscribers,client_infos,all_client_infos,handle_command))
);

cljs.core.add_watch(status,cljs.core.cst$kw$org$numenta$sanity$comportex$simulation_SLASH_push_DASH_to_DASH_subscribers,((function (status,status_subscribers,client_infos,all_client_infos,handle_command){
return (function (_,___$1,___$2,v){
var seq__68759 = cljs.core.seq((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(status_subscribers) : cljs.core.deref.call(null,status_subscribers)));
var chunk__68760 = null;
var count__68761 = (0);
var i__68762 = (0);
while(true){
if((i__68762 < count__68761)){
var ch = chunk__68760.cljs$core$IIndexed$_nth$arity$2(null,i__68762);
cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(ch,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [v], null));

var G__68805 = seq__68759;
var G__68806 = chunk__68760;
var G__68807 = count__68761;
var G__68808 = (i__68762 + (1));
seq__68759 = G__68805;
chunk__68760 = G__68806;
count__68761 = G__68807;
i__68762 = G__68808;
continue;
} else {
var temp__4657__auto__ = cljs.core.seq(seq__68759);
if(temp__4657__auto__){
var seq__68759__$1 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(seq__68759__$1)){
var c__6956__auto__ = cljs.core.chunk_first(seq__68759__$1);
var G__68809 = cljs.core.chunk_rest(seq__68759__$1);
var G__68810 = c__6956__auto__;
var G__68811 = cljs.core.count(c__6956__auto__);
var G__68812 = (0);
seq__68759 = G__68809;
chunk__68760 = G__68810;
count__68761 = G__68811;
i__68762 = G__68812;
continue;
} else {
var ch = cljs.core.first(seq__68759__$1);
cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(ch,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [v], null));

var G__68813 = cljs.core.next(seq__68759__$1);
var G__68814 = null;
var G__68815 = (0);
var G__68816 = (0);
seq__68759 = G__68813;
chunk__68760 = G__68814;
count__68761 = G__68815;
i__68762 = G__68816;
continue;
}
} else {
return null;
}
}
break;
}
});})(status,status_subscribers,client_infos,all_client_infos,handle_command))
);

var c__38109__auto__ = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto__,status,status_subscribers,client_infos,all_client_infos,handle_command){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto__,status,status_subscribers,client_infos,all_client_infos,handle_command){
return (function (state_68784){
var state_val_68785 = (state_68784[(1)]);
if((state_val_68785 === (7))){
var inst_68768 = (state_68784[(7)]);
var inst_68768__$1 = (state_68784[(2)]);
var inst_68769 = (inst_68768__$1 == null);
var inst_68770 = cljs.core.not(inst_68769);
var state_68784__$1 = (function (){var statearr_68786 = state_68784;
(statearr_68786[(7)] = inst_68768__$1);

return statearr_68786;
})();
if(inst_68770){
var statearr_68787_68817 = state_68784__$1;
(statearr_68787_68817[(1)] = (8));

} else {
var statearr_68788_68818 = state_68784__$1;
(statearr_68788_68818[(1)] = (9));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_68785 === (1))){
var state_68784__$1 = state_68784;
var statearr_68789_68819 = state_68784__$1;
(statearr_68789_68819[(2)] = null);

(statearr_68789_68819[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_68785 === (4))){
var state_68784__$1 = state_68784;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_68784__$1,(7),commands);
} else {
if((state_val_68785 === (6))){
var inst_68780 = (state_68784[(2)]);
var state_68784__$1 = state_68784;
var statearr_68790_68820 = state_68784__$1;
(statearr_68790_68820[(2)] = inst_68780);

(statearr_68790_68820[(1)] = (3));


return cljs.core.cst$kw$recur;
} else {
if((state_val_68785 === (3))){
var inst_68782 = (state_68784[(2)]);
var state_68784__$1 = state_68784;
return cljs.core.async.impl.ioc_helpers.return_chan(state_68784__$1,inst_68782);
} else {
if((state_val_68785 === (2))){
var inst_68764 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(sim_closed_QMARK_) : cljs.core.deref.call(null,sim_closed_QMARK_));
var inst_68765 = cljs.core.not(inst_68764);
var state_68784__$1 = state_68784;
if(inst_68765){
var statearr_68791_68821 = state_68784__$1;
(statearr_68791_68821[(1)] = (4));

} else {
var statearr_68792_68822 = state_68784__$1;
(statearr_68792_68822[(1)] = (5));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_68785 === (9))){
var inst_68775 = (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(sim_closed_QMARK_,true) : cljs.core.reset_BANG_.call(null,sim_closed_QMARK_,true));
var state_68784__$1 = state_68784;
var statearr_68793_68823 = state_68784__$1;
(statearr_68793_68823[(2)] = inst_68775);

(statearr_68793_68823[(1)] = (10));


return cljs.core.cst$kw$recur;
} else {
if((state_val_68785 === (5))){
var state_68784__$1 = state_68784;
var statearr_68794_68824 = state_68784__$1;
(statearr_68794_68824[(2)] = null);

(statearr_68794_68824[(1)] = (6));


return cljs.core.cst$kw$recur;
} else {
if((state_val_68785 === (10))){
var inst_68777 = (state_68784[(2)]);
var state_68784__$1 = state_68784;
var statearr_68795_68825 = state_68784__$1;
(statearr_68795_68825[(2)] = inst_68777);

(statearr_68795_68825[(1)] = (6));


return cljs.core.cst$kw$recur;
} else {
if((state_val_68785 === (8))){
var inst_68768 = (state_68784[(7)]);
var inst_68772 = (handle_command.cljs$core$IFn$_invoke$arity$1 ? handle_command.cljs$core$IFn$_invoke$arity$1(inst_68768) : handle_command.call(null,inst_68768));
var state_68784__$1 = (function (){var statearr_68796 = state_68784;
(statearr_68796[(8)] = inst_68772);

return statearr_68796;
})();
var statearr_68797_68826 = state_68784__$1;
(statearr_68797_68826[(2)] = null);

(statearr_68797_68826[(1)] = (2));


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
});})(c__38109__auto__,status,status_subscribers,client_infos,all_client_infos,handle_command))
;
return ((function (switch__37995__auto__,c__38109__auto__,status,status_subscribers,client_infos,all_client_infos,handle_command){
return (function() {
var org$numenta$sanity$comportex$simulation$handle_commands_$_state_machine__37996__auto__ = null;
var org$numenta$sanity$comportex$simulation$handle_commands_$_state_machine__37996__auto____0 = (function (){
var statearr_68801 = [null,null,null,null,null,null,null,null,null];
(statearr_68801[(0)] = org$numenta$sanity$comportex$simulation$handle_commands_$_state_machine__37996__auto__);

(statearr_68801[(1)] = (1));

return statearr_68801;
});
var org$numenta$sanity$comportex$simulation$handle_commands_$_state_machine__37996__auto____1 = (function (state_68784){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_68784);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e68802){if((e68802 instanceof Object)){
var ex__37999__auto__ = e68802;
var statearr_68803_68827 = state_68784;
(statearr_68803_68827[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_68784);

return cljs.core.cst$kw$recur;
} else {
throw e68802;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__68828 = state_68784;
state_68784 = G__68828;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$comportex$simulation$handle_commands_$_state_machine__37996__auto__ = function(state_68784){
switch(arguments.length){
case 0:
return org$numenta$sanity$comportex$simulation$handle_commands_$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$comportex$simulation$handle_commands_$_state_machine__37996__auto____1.call(this,state_68784);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$comportex$simulation$handle_commands_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$comportex$simulation$handle_commands_$_state_machine__37996__auto____0;
org$numenta$sanity$comportex$simulation$handle_commands_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$comportex$simulation$handle_commands_$_state_machine__37996__auto____1;
return org$numenta$sanity$comportex$simulation$handle_commands_$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto__,status,status_subscribers,client_infos,all_client_infos,handle_command))
})();
var state__38111__auto__ = (function (){var statearr_68804 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_68804[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto__);

return statearr_68804;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto__,status,status_subscribers,client_infos,all_client_infos,handle_command))
);

return c__38109__auto__;
});
org.numenta.sanity.comportex.simulation.start = (function org$numenta$sanity$comportex$simulation$start(steps_c,model_atom,world_c,commands_c,htm_step){
var options_68831 = (function (){var G__68830 = new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$go_QMARK_,false,cljs.core.cst$kw$step_DASH_ms,(20),cljs.core.cst$kw$force_DASH_n_DASH_steps,(0)], null);
return (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(G__68830) : cljs.core.atom.call(null,G__68830));
})();
var sim_closed_QMARK__68832 = (cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(false) : cljs.core.atom.call(null,false));
if(cljs.core.truth_(commands_c)){
org.numenta.sanity.comportex.simulation.handle_commands(commands_c,model_atom,options_68831,sim_closed_QMARK__68832);
} else {
}

org.numenta.sanity.comportex.simulation.simulation_loop(model_atom,world_c,steps_c,options_68831,sim_closed_QMARK__68832,htm_step);

return null;
});
