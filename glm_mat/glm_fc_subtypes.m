clear

networks = {'CER','LIM','MOT','VIS','DMN','FP','VATTSAL'}

function results = subtype_fc_glm(data_mat)
 data_ = [];
 data  = load(data_mat);
 data_.x = double(data.x);
 data_.y = double((data.y));
 data_.c = [0,1];

 opt_glm.test = 'ttest';

 results =  niak_glm(data_,opt_glm);

end


pce_arr = [];
ttest_arr = [];
f2_arr = [];

subtypes_str = [];


for net = networks
	file = ['*' net{1} '.mat']
	disp(net)
	files = dir((file));
	for i=1:length(files)
	    data_mat = files(i).name;
	    data_str = strsplit(data_mat,".");
	    subtypes_str = [subtypes_str data_str(1)];
		
	    result = subtype_fc_glm(data_mat);  
	    pce_arr = [pce_arr result.pce(2)];
	    ttest_arr = [ttest_arr result.ttest(2)];
	    f2_arr = [f2_arr result.f2];	    
	end
end
%subtypes_str(1) = [];


opt.labels_x = subtypes_str;
opt.labels_y = {'ttest','pce'};
glm_output = transpose(cat(1,ttest_arr,pce_arr));

niak_write_csv('glm_output.csv',glm_output,opt)




