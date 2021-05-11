from .models.motion_vae import *
from .trainer.vae_trainer import *
from .utils.plot_script import *
from .utils.paramUtil import *
from .utils.utils_ import *
from .options.evaluate_vae_options import *
from .dataProcessing import dataset
from torch.utils.data import DataLoader
from scipy.spatial.transform import Rotation as R


def character_matrix(animation_n):

	parser = TestOptions()
	opt = parser.parse()

	device = torch.device("cuda:" + str(opt.gpu_id) if opt.gpu_id else "cpu")
	#device = torch.device("cuda:0")

	opt.save_root = os.path.join(opt.checkpoints_dir, opt.dataset_type, opt.name)
	opt.model_path = os.path.join(opt.save_root, 'model')

	model_file_path = os.path.dirname(os.path.dirname(__file__)) + '\\Action2Motion_OnBlender\\checkpoints\\vae\\humanact12\\vanila_vae_tf\\model\\latest.tar'

	input_size = 72
	joints_num = 24
	label_dec = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
	raw_offsets = humanact12_raw_offsets
	kinematic_chain = humanact12_kinematic_chain
	enumerator = humanact12_coarse_action_enumerator

	opt.dim_category = len(label_dec)
	opt.pose_dim = input_size
	opt.input_size = input_size + opt.dim_category
	opt.output_size = input_size

	model = torch.load(model_file_path, map_location='cuda:0')
	
	prior_net = GaussianGRU(opt.input_size, opt.dim_z, opt.hidden_size,
										opt.prior_hidden_layers, opt.num_samples, device)

	decoder = DecoderGRU(opt.input_size + opt.dim_z, opt.output_size, opt.hidden_size,
										opt.decoder_hidden_layers,
										opt.num_samples, device)
	prior_net.load_state_dict(model['prior_net'])
	decoder.load_state_dict(model['decoder'])
	prior_net.to(device)
	decoder.to(device)
	trainer = Trainer(None, opt, device)

	categories = np.arange(opt.dim_category).repeat(opt.replic_times, axis=0)
	num_samples = categories.shape[0]
	category_oh, classes = trainer.get_cate_one_hot(categories)
	fake_motion, _ = trainer.evaluate(prior_net, decoder, num_samples, category_oh)
	fake_motion = fake_motion.cpu().numpy()

	#print(fake_motion.shape) #Da togliere

	motion_orig = fake_motion[animation_n]

	offset = np.matlib.repmat(np.array([motion_orig[0, 0], motion_orig[0, 1], motion_orig[0, 2]]),
									motion_orig.shape[0], joints_num)

	motion_mat = motion_orig - offset
	motion_mat = motion_mat.reshape(-1, joints_num, 3)


	
	#Inizio Rotazione degli assi
	rotation_degrees = -90
	rotation_radians = np.radians(rotation_degrees)
	rotation_axis = np.array([1, 0, 0])
	rotation_vector = rotation_radians * rotation_axis
	rotation = R.from_rotvec(rotation_vector)
	
	for m in motion_mat:
		for i, vec in enumerate(m):

			rotated_vec = rotation.apply(vec)
			#rotated_vec[2]=rotated_vec[2]+1
			m[i] = rotated_vec
			#Fine Rotazione degli assi


	return motion_mat #Restituisce la matrice [60,24,3] (dove 60 sono i frame, 24 i joints e 3 le coordinate x y z)