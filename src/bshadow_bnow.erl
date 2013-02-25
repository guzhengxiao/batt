-module( bshadow_bnow ).
-compile(export_all).

-define(CHECK_BNOW_DEBUG_STATUS , 
    case ?BNOW_DEBUG_STATUS of
        undefined -> ok
        ;_ -> 
            {ok , _Len} = application:get_env( bnow,debug_mode_msg_length )
            ,if
                _Len =:= 0 -> 
                    application:unset_env(bnow,  debug_mode )
                    ,application:unset_env(bnow,  debug_mode_msg_length )
                    ,erase( bnow_debug_mode )
                ;true -> 
                    application:set_env(bnow,debug_mode,_Len - 1)
            end
    end
).
-define(BNOW_DEBUG_STATUS , 
    case get(bnow_debug_mode) of
        undefined ->
            _R = application:get_env( bnow , debug_mode )
            ,put(bnow_debug_mode , _R)
            ,_R
        ;_HasDebugMode -> _HasDebugMode
    end
).

start_debug(Len) ->
    application:set_env(bnow , debug_mode , true),
    application:set_env(bnow , debug_mode_msg_length , Len).
    
