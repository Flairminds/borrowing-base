import { createSlice } from '@reduxjs/toolkit';

const initialState = {
	inProgressStatus: false
};

const diExtractionSlice = createSlice({
	name: 'diExtractionStatus',
	initialState,
	reducers: {
		setExtractionStatus: (state, action) => {
			state.inProgressStatus = action.payload;
		}
	}
});

export const { setExtractionStatus } = diExtractionSlice.actions;
export default diExtractionSlice.reducer;
