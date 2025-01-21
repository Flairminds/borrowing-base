import { createSlice } from '@reduxjs/toolkit';

const initialState = {
	name: '',
	id: ''
};

export const baseFileData = createSlice({
	name: 'baseFileData',
	initialState,
	reducers: {
		updateBaseFileName: (state, action) => {
			state.name = action.payload;
		},
		updateBaseFileId: (state, action) => {
			state.id = action.payload;
		},
		updateBaseFileData: (state, action) => {
			state = action.payload;
		}
	}
});

export const {updateBaseFileName, updateBaseFileId, updateBaseFileData} = baseFileData.actions;
export default baseFileData.reducer;