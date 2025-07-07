function scrapeStudentNumbers() {
  // STEP 1: Update column index - change 0 to match your student number column
  const STUDENT_NUMBER_COLUMN = 0; // careful! this is zero indexed
  
  // Persian to English number mapping
  const persianToEnglishMap = {
    '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
    '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9'
  };
  
  const convertNumbers = (text) => {
    return text.replace(/[۰-۹]/g, char => persianToEnglishMap[char] || char);
  };

  const studentNumbers = [];
  let found = 0;
  
  // Find all table rows
  const rows = document.querySelectorAll('table tr');
  
  rows.forEach(row => {
    const cells = row.querySelectorAll('td');
    // Only process rows with enough columns
    if(cells.length > STUDENT_NUMBER_COLUMN) {
      let num = cells[STUDENT_NUMBER_COLUMN].textContent.trim();
      
      // Convert Persian numbers to English
      num = convertNumbers(num);
      
      studentNumbers.push(num);
      found++;
    }
  });
  
  console.log('✅ Found ' + found + ' student numbers');
  console.log('📋 Copy the array below and paste into submitted.json:');
  console.log(JSON.stringify(studentNumbers));
  console.log('⚠️  If these look wrong:');
  console.log('1. Change STUDENT_NUMBER_COLUMN value in this script');
  console.log('2. Reload page and run script again');
  
  return studentNumbers;
}

// Run automatically
scrapeStudentNumbers();