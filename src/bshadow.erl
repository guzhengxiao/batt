-module( bshadow ).
-export([start/0, init/0 , store/3 , fetch/2, fold/2]).

start()->
    application:start(bshadow).

init() -> 
    case ets:info(bshadow_msg) of
        undefined -> ets:new(bshadow_msg , [named_table , ordered_set, public])
        ;_ -> ok
    end
    ,ok.

store( Key , Time , Msg ) when is_binary(Key ) andalso is_integer(Time) andalso is_binary(Msg) ->
    ets:insert(bshadow_msg , { { Key , Time } , Msg })
;store( _ , _ , _ ) -> badargs.

fetch( Key , Time ) when is_binary(Key) andalso is_integer(Time) ->
    Rs = ets:lookup(bshadow_msg , { Key , Time } )
    ,if 
        Rs =:= [{{Key , Time} , undefined}] -> [] 
        ;true -> Rs 
    end
;fetch(_,_) -> badargs.

fold(  {Key,Time} = Start , Len ) when is_binary(Key) andalso is_integer(Time) andalso is_integer(Len) ->
    ets:insert_new(bshadow_msg , {Start , undefined} )
    ,fold( Start ,Len ,[])
;fold( _ , _ ) -> badargs.
    
fold(K , L , R) when K =:= '$end_of_table' orelse L =< 0 ->
    R
;fold(K , L , R) -> 
    case ets:lookup( bshadow_msg, K ) of
        [] -> fold( ets:next( bshadow_msg , K ) , L , R)
        ;[{_ , undefined}] -> fold( ets:next(bshadow_msg , K ) , L,R)
        ;V -> fold( ets:next(bshadow_msg , K) , L -1 , R++V )
    end.

