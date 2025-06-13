import { configureStore } from '@reduxjs/toolkit';
import BaseFileDataSlice from './slices/baseFileData';
import diExtractionReducer from './slices/uploadFileStatus';

export const store = configureStore({
	reducer: {
		baseFileData: BaseFileDataSlice,
		diExtractionStatus: diExtractionReducer
	}
});