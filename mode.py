if(__name__=="__main__"):
    import argparse


    parser=argparse.ArgumentParser(
        usage="""

    1-first time to create modes you should run the following and the script check if mode initialized before or not and it not will create some files and folders and after finishing his job open the default editor for adding files to be render ,build files (like hex .lss etc), enable_cache_desired_files, builed command after
    `python mode.py init`
    then the following command to create modes and the script check if mode initialized before if not  else make sure that no mode is dupicated 
    note that set name will make tags like the following
    set_name_1 set_name_2 set_name_3 etc
    `python mode.py create_mode --mode_name set_name --set_range 1:XXX`
    or just single mode 
    `python mode.py create_mode --mode_name mode_name`
    but open its json in editor as usally be a spcial one

    2-after running all of above you will be on template mode to check what mode you are on run the following
    `python mode.py get_current_mode`

    3-if you want to modify any mode json run the following command
    `python mode.py modify_mode --mode_num mode_num --vim`
    and will open its render json in default editor in your system and vim flag is optional for me :D

    4-to switch the current mode run the following
    `python mode.py switch --mode_num mode_num --build`

    5-for rendering specific mode in its cache
    `python mode.py render --mode_name mode_name`
    or the following to render all modes in each mode cache
    `python mode.py render --mode_name *`

    6- for building specific mode in its cache
    `python mode.py build --mode_num mode_name` 
    or for building all modes in each cache in series
    `python mode.py build --mode_num *` 


        """,
        description="""
        Description : Automate source code editing for integration test by make the developing source code as template where any line of code surrounded with comment like following:
    """
        )

    mode_actions='init create_mode get_config get_modes get_current_mode modify_config add remove modify_mode switch render build'.split(' ')
    parser.add_argument('action',type=str,choices=mode_actions)
    parser.add_argument('-m','--mode_name',type=str)
    parser.add_argument('-v','--vim',action='store_true',default=False)
    parser.add_argument('-b','--build',action='store_true',default=False)
    parser.add_argument('-r','--render',action='store_true',default=False)
    parser.add_argument('-s','--set_range',type=str,default='')
    parser.add_argument('-f','--files',type=str,default='')
    args=parser.parse_args()   
    import json ,subprocess,os,re,pystache
    file_name_pattern=r'(?P<file_name>[\w\d]+\.[\w\d]+)$'

    def get_template_path(file_name):
        return os.sep.join(['.','.mode','template',file_name])
    def get_mode_render_config_path(mode_name):
        return os.sep.join(['.','.mode',mode_name,'render_config.json'])

    def change_current_mode(mode_name):
        cfg['current_mode']=mode_name
        with open(os.sep.join(['.mode','config.json']),'w') as f:
            json.dump(cfg,f)
        pass

    def render_mode_to_work_tree(mode_name:str):
        for file in cfg['file_paths']:
            file_name=re.match(file_name_pattern,file).group('file_name')
            with open(get_mode_render_config_path(args.mode_name),'r') as f:
                render_cfg=json.load(f)
            with open(file,'w') as f:
                f.write(
                    pystache.Renderer().render_path(get_template_path(file),render_cfg)
                )
        pass

    def get_modes():
        print(cfg['mode'])

    def create_mode(mode_name):
        mode_path=os.sep.join(['.','.mode',mode_name])
        subprocess.check_call(('mkdir %s'%mode_path).split(),stdout=subprocess.PIPE)
        with open(mode_path+os.sep+'render_config.json','w') as f:
            f.write('{\"%s\":true}'%mode_name)
            pass
        cfg['mode'].append(mode_name) 
        with open(os.sep.join(['.mode','config.json']),'w') as f:
            json.dump(cfg,f)
            pass
        pass

    if(not args.action=='init'):
        with open(os.sep.join(['.','.mode','config.json']),'r') as f:
            cfg=json.load(f)
        pass # end of action
    if(args.action=='init'):
        if(not os.path.exists('./.mode')  ): # case initialized mode
            subprocess.check_call('mkdir ./.mode'.split(),stdout=subprocess.PIPE)
            with open('./.mode/config.json','w') as config:
                config.write('''
                {
                    "file_paths":[],
                    "build_paths":[],
                    "cache_build_paths":false,
                    "cache_rendered_paths":false,
                    "mode":
                    [
                        "template"
                    ],
                    "current_mode":"template"
                }''')
                pass
            subprocess.check_call('mkdir ./.mode/template'.split(),stdout=subprocess.PIPE)

            with open('.'+os.sep+'.mode'+os.sep+'config.json','r') as f:
                cfg=json.load(f)
                pass

            create_mode("dev")
            print('mode init successfull\n modes = %s\n current mode is %s'%(
                    str(cfg['mode']),
                    cfg['current_mode']
                    )
                )
            pass
        else: # case initialized before
            print('initialized before')
            pass                
        pass # end of action

    elif(args.action=='get_modes'):
        get_modes()
        pass # end of action

    elif(args.action=='create_mode'):
        if(bool(args.set_range)):
            _=args.set_range.split(':')
            if len(_)!=2:
                raise('invalid set_range input should like 1:435345  ')
                pass
            else:
                for mode_num in range(int(_[0]),int(_[1])+1):
                    create_mode(args.mode_name+str(mode_num))
                    pass
                pass
            pass # end of action
        else:
            create_mode(args.mode_name)
            pass
        pass # end of action
    elif(args.action=='get_current_mode'):
        with open('.'+os.sep+'.mode'+os.sep+'config.json','r') as f:
            print(json.load(f)['current_mode'])
        pass# end of script
    elif(args.action=='get_config'):
        with open('.'+os.sep+'.mode'+os.sep+'config.json','r') as f:
            from pprint import pprint
            pprint(json.load(f))
            pass
    elif(args.action=='modify_mode'):
        if(os.path.exists(get_mode_render_config_path(args.mode_name))):
            os.system(('vim ' if args.vim else '' )+get_mode_render_config_path(args.mode_name))
            pass 
        pass # end of action
    elif(args.action=='add'):
        if(os.path.exists('.'+os.sep+'.mode'+os.sep+'config.json')):
            cfg['file_paths']=cfg['file_paths']+args.files.split(',')
            with open(os.sep.join(['.mode','config.json']),'w') as f:
                json.dump(cfg,f)
            pass
        pass 
    elif(args.action=='remove'):
        if(os.path.exists('.'+os.sep+'.mode'+os.sep+'config.json')):
            for file in args.files.split(','):
                cfg['file_paths'].pop(cfg['file_paths'].index(file))
            with open(os.sep.join(['.mode','config.json']),'w') as f:
                json.dump(cfg,f)
            pass
        pass 
    elif(args.action=='modify_config'):
        if(os.path.exists('.'+os.sep+'.mode'+os.sep+'config.json')):
            os.system(('vim ' if args.vim else '' )+('.'+os.sep+'.mode'+os.sep+'config.json'))
            pass # end of action
    elif(args.action=='switch'):
        if(cfg['current_mode'] == 'template' and args.mode_name != 'template'):
            for file in cfg['file_paths']:
                file_name=re.match(file_name_pattern,file).group('file_name')
                subprocess.check_call(('mv -f %s %s'%(
                    file,
                    os.sep.join(['.','.mode',cfg['current_mode'],file_name]))).split(),stdout=subprocess.PIPE)                
            pass
        pass # end of action
        render_mode_to_work_tree(args.mode_name)
        change_current_mode(args.mode_name)
        pass
    elif(args.action=='render'):
        print('not inplemented yet')
        pass
    elif(args.action=='build'):
        print('not inplemented yet')
        pass
    pass # end of script