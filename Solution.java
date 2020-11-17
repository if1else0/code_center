class Solution {
    
    public int findMaxConsecutiveOnes(int[] nums) {
        int result = -1;
        int length = nums.length;
        if(length <= 0 || length > 10000 ){
            return -1;
        }   
        
        int count = 0;
        int maxCount = 0;
        
        for(int i=0; i <= length-1; i++){
            if(nums[i] == 1){
                count++;
            }else{
                if(count > maxCount){
                    maxCount = count;
                }
                count=0;
            }    
        }
        
        result = (maxCount>count?maxCount:count);
        return result;
    }
    
     
}
