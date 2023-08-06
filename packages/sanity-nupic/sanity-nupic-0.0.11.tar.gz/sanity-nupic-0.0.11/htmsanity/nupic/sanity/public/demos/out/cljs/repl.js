// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('cljs.repl');
goog.require('cljs.core');
cljs.repl.print_doc = (function cljs$repl$print_doc(m){
cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["-------------------------"], 0));

cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([[cljs.core.str((function (){var temp__4657__auto__ = cljs.core.cst$kw$ns.cljs$core$IFn$_invoke$arity$1(m);
if(cljs.core.truth_(temp__4657__auto__)){
var ns = temp__4657__auto__;
return [cljs.core.str(ns),cljs.core.str("/")].join('');
} else {
return null;
}
})()),cljs.core.str(cljs.core.cst$kw$name.cljs$core$IFn$_invoke$arity$1(m))].join('')], 0));

if(cljs.core.truth_(cljs.core.cst$kw$protocol.cljs$core$IFn$_invoke$arity$1(m))){
cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["Protocol"], 0));
} else {
}

if(cljs.core.truth_(cljs.core.cst$kw$forms.cljs$core$IFn$_invoke$arity$1(m))){
var seq__65822_65836 = cljs.core.seq(cljs.core.cst$kw$forms.cljs$core$IFn$_invoke$arity$1(m));
var chunk__65823_65837 = null;
var count__65824_65838 = (0);
var i__65825_65839 = (0);
while(true){
if((i__65825_65839 < count__65824_65838)){
var f_65840 = chunk__65823_65837.cljs$core$IIndexed$_nth$arity$2(null,i__65825_65839);
cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["  ",f_65840], 0));

var G__65841 = seq__65822_65836;
var G__65842 = chunk__65823_65837;
var G__65843 = count__65824_65838;
var G__65844 = (i__65825_65839 + (1));
seq__65822_65836 = G__65841;
chunk__65823_65837 = G__65842;
count__65824_65838 = G__65843;
i__65825_65839 = G__65844;
continue;
} else {
var temp__4657__auto___65845 = cljs.core.seq(seq__65822_65836);
if(temp__4657__auto___65845){
var seq__65822_65846__$1 = temp__4657__auto___65845;
if(cljs.core.chunked_seq_QMARK_(seq__65822_65846__$1)){
var c__6956__auto___65847 = cljs.core.chunk_first(seq__65822_65846__$1);
var G__65848 = cljs.core.chunk_rest(seq__65822_65846__$1);
var G__65849 = c__6956__auto___65847;
var G__65850 = cljs.core.count(c__6956__auto___65847);
var G__65851 = (0);
seq__65822_65836 = G__65848;
chunk__65823_65837 = G__65849;
count__65824_65838 = G__65850;
i__65825_65839 = G__65851;
continue;
} else {
var f_65852 = cljs.core.first(seq__65822_65846__$1);
cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["  ",f_65852], 0));

var G__65853 = cljs.core.next(seq__65822_65846__$1);
var G__65854 = null;
var G__65855 = (0);
var G__65856 = (0);
seq__65822_65836 = G__65853;
chunk__65823_65837 = G__65854;
count__65824_65838 = G__65855;
i__65825_65839 = G__65856;
continue;
}
} else {
}
}
break;
}
} else {
if(cljs.core.truth_(cljs.core.cst$kw$arglists.cljs$core$IFn$_invoke$arity$1(m))){
var arglists_65857 = cljs.core.cst$kw$arglists.cljs$core$IFn$_invoke$arity$1(m);
if(cljs.core.truth_((function (){var or__6153__auto__ = cljs.core.cst$kw$macro.cljs$core$IFn$_invoke$arity$1(m);
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return cljs.core.cst$kw$repl_DASH_special_DASH_function.cljs$core$IFn$_invoke$arity$1(m);
}
})())){
cljs.core.prn.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([arglists_65857], 0));
} else {
cljs.core.prn.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([((cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$sym$quote,cljs.core.first(arglists_65857)))?cljs.core.second(arglists_65857):arglists_65857)], 0));
}
} else {
}
}

if(cljs.core.truth_(cljs.core.cst$kw$special_DASH_form.cljs$core$IFn$_invoke$arity$1(m))){
cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["Special Form"], 0));

cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([" ",cljs.core.cst$kw$doc.cljs$core$IFn$_invoke$arity$1(m)], 0));

if(cljs.core.contains_QMARK_(m,cljs.core.cst$kw$url)){
if(cljs.core.truth_(cljs.core.cst$kw$url.cljs$core$IFn$_invoke$arity$1(m))){
return cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([[cljs.core.str("\n  Please see http://clojure.org/"),cljs.core.str(cljs.core.cst$kw$url.cljs$core$IFn$_invoke$arity$1(m))].join('')], 0));
} else {
return null;
}
} else {
return cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([[cljs.core.str("\n  Please see http://clojure.org/special_forms#"),cljs.core.str(cljs.core.cst$kw$name.cljs$core$IFn$_invoke$arity$1(m))].join('')], 0));
}
} else {
if(cljs.core.truth_(cljs.core.cst$kw$macro.cljs$core$IFn$_invoke$arity$1(m))){
cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["Macro"], 0));
} else {
}

if(cljs.core.truth_(cljs.core.cst$kw$repl_DASH_special_DASH_function.cljs$core$IFn$_invoke$arity$1(m))){
cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq(["REPL Special Function"], 0));
} else {
}

cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([" ",cljs.core.cst$kw$doc.cljs$core$IFn$_invoke$arity$1(m)], 0));

if(cljs.core.truth_(cljs.core.cst$kw$protocol.cljs$core$IFn$_invoke$arity$1(m))){
var seq__65826 = cljs.core.seq(cljs.core.cst$kw$methods.cljs$core$IFn$_invoke$arity$1(m));
var chunk__65827 = null;
var count__65828 = (0);
var i__65829 = (0);
while(true){
if((i__65829 < count__65828)){
var vec__65830 = chunk__65827.cljs$core$IIndexed$_nth$arity$2(null,i__65829);
var name = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__65830,(0),null);
var map__65831 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__65830,(1),null);
var map__65831__$1 = ((((!((map__65831 == null)))?((((map__65831.cljs$lang$protocol_mask$partition0$ & (64))) || (map__65831.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__65831):map__65831);
var doc = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__65831__$1,cljs.core.cst$kw$doc);
var arglists = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__65831__$1,cljs.core.cst$kw$arglists);
cljs.core.println();

cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([" ",name], 0));

cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([" ",arglists], 0));

if(cljs.core.truth_(doc)){
cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([" ",doc], 0));
} else {
}

var G__65858 = seq__65826;
var G__65859 = chunk__65827;
var G__65860 = count__65828;
var G__65861 = (i__65829 + (1));
seq__65826 = G__65858;
chunk__65827 = G__65859;
count__65828 = G__65860;
i__65829 = G__65861;
continue;
} else {
var temp__4657__auto__ = cljs.core.seq(seq__65826);
if(temp__4657__auto__){
var seq__65826__$1 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(seq__65826__$1)){
var c__6956__auto__ = cljs.core.chunk_first(seq__65826__$1);
var G__65862 = cljs.core.chunk_rest(seq__65826__$1);
var G__65863 = c__6956__auto__;
var G__65864 = cljs.core.count(c__6956__auto__);
var G__65865 = (0);
seq__65826 = G__65862;
chunk__65827 = G__65863;
count__65828 = G__65864;
i__65829 = G__65865;
continue;
} else {
var vec__65833 = cljs.core.first(seq__65826__$1);
var name = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__65833,(0),null);
var map__65834 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__65833,(1),null);
var map__65834__$1 = ((((!((map__65834 == null)))?((((map__65834.cljs$lang$protocol_mask$partition0$ & (64))) || (map__65834.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__65834):map__65834);
var doc = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__65834__$1,cljs.core.cst$kw$doc);
var arglists = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__65834__$1,cljs.core.cst$kw$arglists);
cljs.core.println();

cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([" ",name], 0));

cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([" ",arglists], 0));

if(cljs.core.truth_(doc)){
cljs.core.println.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([" ",doc], 0));
} else {
}

var G__65866 = cljs.core.next(seq__65826__$1);
var G__65867 = null;
var G__65868 = (0);
var G__65869 = (0);
seq__65826 = G__65866;
chunk__65827 = G__65867;
count__65828 = G__65868;
i__65829 = G__65869;
continue;
}
} else {
return null;
}
}
break;
}
} else {
return null;
}
}
});
