function varargout = Slider_test_v2(varargin)
% SLIDER_TEST_V2 MATLAB code for Slider_test_v2.fig
%      SLIDER_TEST_V2, by itself, creates a new SLIDER_TEST_V2 or raises the existing
%      singleton*.
%
%      H = SLIDER_TEST_V2 returns the handle to a new SLIDER_TEST_V2 or the handle to
%      the existing singleton*.
%
%      SLIDER_TEST_V2('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in SLIDER_TEST_V2.M with the given input arguments.
%
%      SLIDER_TEST_V2('Property','Value',...) creates a new SLIDER_TEST_V2 or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before Slider_test_v2_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to Slider_test_v2_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help Slider_test_v2

% Last Modified by GUIDE v2.5 12-Nov-2018 14:25:12

% Begin initialization code - DO NOT EDIT
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
% End initialization code - DO NOT EDIT


% --- Executes just before Slider_test_v2 is made visible.
function Slider_test_v2_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to Slider_test_v2 (see VARARGIN)

% Choose default command line output for Slider_test_v2
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes Slider_test_v2 wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = Slider_test_v2_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
global Port;
Port = serial('/dev/ttyUSB5');
set(Port,'BaudRate',115200);
fopen(Port);
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes on button press in pushbutton2.
function pushbutton2_Callback(hObject, eventdata, handles)
global Port;
k=2;
fwrite(Port,k,'int8');

% hObject    handle to pushbutton2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes on slider movement.
function slider1_Callback(hObject, eventdata, handles)
global Port;
valor = get(hObject,'value');
Pushvalor = get(hObject,'value');
fwrite(Port,Pushvalor);
set(handles.texto,'string',num2str(valor));
guidata(hObject,handles);


% --- Executes during object creation, after setting all properties.
function slider1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to slider1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end



function texto_Callback(hObject, eventdata, handles)
edit=get(hObject,'string');
set(handles.slider1,'value',str2num(edit));
guidata(hObject,handles);


% --- Executes during object creation, after setting all properties.
function texto_CreateFcn(hObject, eventdata, handles)
% hObject    handle to texto (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in Fclose.
function Fclose_Callback(hObject, eventdata, handles)
global Port;
fclose(Port);
% hObject    handle to Fclose (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
