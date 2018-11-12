function varargout = Slider_test_v2(varargin)

gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @Slider_test_v2_OpeningFcn, ...
                   'gui_OutputFcn',  @Slider_test_v2_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end



% --- Executes just before Slider_test_v2 is made visible.
function Slider_test_v2_OpeningFcn(hObject, eventdata, handles, varargin)
handles.output = hObject;
guidata(hObject, handles);




% --- Outputs from this function are returned to the command line.
function varargout = Slider_test_v2_OutputFcn(hObject, eventdata, handles) 
varargout{1} = handles.output;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                   port connection                      %
%                                                        %
%you need to select the port to which Serial is connected%
%                                                        %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function pushbutton1_Callback(hObject, eventdata, handles)
global Port;
Port = serial('/dev/ttyUSB5');%here
set(Port,'BaudRate',115200);
fopen(Port);


%%%%%%%%%%%
%test send%
%%%%%%%%%%%
function pushbutton2_Callback(hObject, eventdata, handles)
global Port;
k=2;
fwrite(Port,k,'int8');



%%%%%%%%%%%%%%%%%%%%%%%%
%   value from slider  %
%%%%%%%%%%%%%%%%%%%%%%%%
function slider1_Callback(hObject, eventdata, handles)
global Port;
valor = get(hObject,'value');
Pushvalor = get(hObject,'value');
fwrite(Port,Pushvalor);
set(handles.texto,'string',num2str(valor));
guidata(hObject,handles);


% --- Executes during object creation, after setting all properties.
function slider1_CreateFcn(hObject, eventdata, handles)

if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Keeps track of what slider transmits%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function texto_Callback(hObject, eventdata, handles)
edit=get(hObject,'string');
set(handles.slider1,'value',str2num(edit));
guidata(hObject,handles);


function texto_CreateFcn(hObject, eventdata, handles)

if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Button to close the port%
%%%%%%%%%%%%%%%%%%%%%%%%%%%
function Fclose_Callback(hObject, eventdata, handles)
global Port;
fclose(Port);

