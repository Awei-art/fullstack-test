<script setup>
import { ref, onMounted } from 'vue';

definePageMeta({
  layout: 'default',
  middleware: 'auth'
});

const config = useRuntimeConfig();
const userCookie = useCookie('user_info');
const isLoading = ref(true);
const isSaving = ref(false);
const saveMessage = ref('');
const errorMessage = ref('');
const showFormSuccessMask = ref(false);
const settingDefaultId = ref(null);
const phoneError = ref('');

// 台灣縣市與鄉鎮資料
const taiwanCities = {
  '基隆市': ['仁愛區', '信義區', '中正區', '中山區', '安樂區', '暖暖區', '七堵區'],
  '台北市': ['中正區', '大同區', '中山區', '松山區', '大安區', '萬華區', '信義區', '士林區', '北投區', '內湖區', '南港區', '文山區'],
  '新北市': ['萬里區', '金山區', '板橋區', '汐止區', '深坑區', '石碇區', '瑞芳區', '平溪區', '雙溪區', '貢寮區', '新店區', '坪林區', '烏來區', '永和區', '中和區', '土城區', '三峽區', '樹林區', '鶯歌區', '三重區', '新莊區', '泰山區', '林口區', '蘆洲區', '五股區', '八里區', '淡水區', '三芝區', '石門區'],
  '桃園市': ['中壢區', '平鎮區', '龍潭區', '楊梅區', '新屋區', '觀音區', '桃園區', '龜山區', '八德區', '大溪區', '復興區', '大園區', '蘆竹區'],
  '新竹市': ['東區', '北區', '香山區'],
  '新竹縣': ['竹北市', '湖口鄉', '新豐鄉', '新埔鎮', '關西鎮', '芎林鄉', '寶山鄉', '竹東鎮', '五峰鄉', '橫山鄉', '尖石鄉', '北埔鄉', '峨眉鄉'],
  '苗栗縣': ['竹南鎮', '頭份市', '三灣鄉', '南庄鄉', '獅潭鄉', '後龍鎮', '通霄鎮', '苑裡鎮', '苗栗市', '造橋鄉', '頭屋鄉', '公館鄉', '大湖鄉', '泰安鄉', '銅鑼鄉', '三義鄉', '西湖鄉', '卓蘭鎮'],
  '台中市': ['中區', '東區', '南區', '西區', '北區', '北屯區', '西屯區', '南屯區', '太平區', '大里區', '霧峰區', '烏日區', '豐原區', '后里區', '石岡區', '東勢區', '和平區', '新社區', '潭子區', '大雅區', '神岡區', '大肚區', '沙鹿區', '龍井區', '梧棲區', '清水區', '大甲區', '外埔區', '大安區'],
  '彰化縣': ['彰化市', '芬園鄉', '花壇鄉', '秀水鄉', '鹿港鎮', '福興鄉', '線西鄉', '和美鎮', '伸港鄉', '員林市', '社頭鄉', '永靖鄉', '埔心鄉', '溪湖鎮', '大村鄉', '埔鹽鄉', '田中鎮', '北斗鎮', '田尾鄉', '埤頭鄉', '溪州鄉', '竹塘鄉', '二林鎮', '大城鄉', '芳苑鄉', '二水鄉'],
  '南投縣': ['南投市', '中寮鄉', '草屯鎮', '國姓鄉', '埔里鎮', '仁愛鄉', '名間鄉', '集集鎮', '水里鄉', '魚池鄉', '信義鄉', '竹山鎮', '鹿谷鄉'],
  '雲林縣': ['斗南鎮', '大埤鄉', '虎尾鎮', '土庫鎮', '褒忠鄉', '東勢鄉', '臺西鄉', '崙背鄉', '麥寮鄉', '斗六市', '林內鄉', '古坑鄉', '莿桐鄉', '西螺鎮', '二崙鄉', '北港鎮', '水林鄉', '口湖鄉', '四湖鄉', '元長鄉'],
  '嘉義市': ['東區', '西區'],
  '嘉義縣': ['番路鄉', '梅山鄉', '竹崎鄉', '阿里山鄉', '中埔鄉', '大埔鄉', '水上鄉', '鹿草鄉', '太保市', '朴子市', '東石鄉', '六腳鄉', '新港鄉', '民雄鄉', '大林鎮', '溪口鄉', '義竹鄉', '布袋鎮'],
  '台南市': ['中西區', '東區', '南區', '北區', '安平區', '安南區', '永康區', '歸仁區', '新化區', '左鎮區', '玉井區', '楠西區', '南化區', '仁德區', '關廟區', '龍崎區', '官田區', '麻豆區', '佳里區', '西港區', '七股區', '將軍區', '學甲區', '北門區', '新營區', '後壁區', '白河區', '東山區', '六甲區', '下營區', '柳營區', '鹽水區', '善化區', '大內區', '山上區', '新市區', '安定區'],
  '高雄市': ['新興區', '前金區', '苓雅區', '鹽埕區', '鼓山區', '旗津區', '前鎮區', '三民區', '楠梓區', '小港區', '左營區', '仁武區', '大社區', '東沙群島', '南沙群島', '岡山區', '路竹區', '阿蓮區', '田寮區', '燕巢區', '橋頭區', '梓官區', '彌陀區', '永安區', '湖內區', '鳳山區', '大寮區', '林園區', '鳥松區', '大樹區', '旗山區', '美濃區', '六龜區', '內門區', '杉林區', '甲仙區', '桃源區', '那瑪夏區', '茂林區'],
  '屏東縣': ['屏東市', '三地門鄉', '霧臺鄉', '瑪家鄉', '九如鄉', '里港鄉', '高樹鄉', '鹽埔鄉', '長治鄉', '麟洛鄉', '竹田鄉', '內埔鄉', '萬丹鄉', '潮州鎮', '泰武鄉', '來義鄉', '萬巒鄉', '崁頂鄉', '新埤鄉', '南州鄉', '林邊鄉', '東港鎮', '琉球鄉', '佳冬鄉', '新園鄉', '枋寮鄉', '枋山鄉', '春日鄉', '獅子鄉', '車城鄉', '牡丹鄉', '恆春鎮', '滿州鄉'],
  '宜蘭縣': ['宜蘭市', '頭城鎮', '礁溪鄉', '壯圍鄉', '員山鄉', '羅東鎮', '三星鄉', '大同鄉', '五結鄉', '冬山鄉', '蘇澳鎮', '南澳鄉'],
  '花蓮縣': ['花蓮市', '新城鄉', '秀林鄉', '吉安鄉', '壽豐鄉', '鳳林鎮', '光復鄉', '豐濱鄉', '瑞穗鄉', '萬榮鄉', '玉里鎮', '卓溪鄉', '富里鄉'],
  '台東縣': ['臺東市', '綠島鄉', '蘭嶼鄉', '延平鄉', '卑南鄉', '鹿野鄉', '關山鎮', '海端鄉', '池上鄉', '東河鄉', '成功鎮', '長濱鄉', '太麻里鄉', '金峰鄉', '大武鄉', '達仁鄉'],
  '澎湖縣': ['馬公市', '西嶼鄉', '望安鄉', '七美鄉', '白沙鄉', '湖西鄉'],
  '金門縣': ['金沙鎮', '金湖鎮', '金寧鄉', '金城鎮', '烈嶼鄉', '烏坵鄉'],
  '連江縣': ['南竿鄉', '北竿鄉', '莒光鄉', '東引鄉']
};

// 地址簿清單
const addresses = ref([]);

// 編輯/新增表單狀態
const showForm = ref(false);
const isEditing = ref(false);
const editingId = ref(null);

// 可用的鄉鎮市區列表 (根據所選的縣市動態變化)
const availableDistricts = computed(() => {
  if (form.value.city && taiwanCities[form.value.city]) {
    return taiwanCities[form.value.city];
  }
  return [];
});

const form = ref({
  title: '',
  receiver_name: '',
  receiver_phone: '',
  city: '台中市', // 預設帶入台中市
  district: '新社區', // 預設帶入新社區
  detail_address: '',
  is_default: false
});

// 重設表單
const resetForm = () => {
  form.value = {
    title: '',
    receiver_name: '',
    receiver_phone: '',
    city: '台中市',
    district: '新社區',
    detail_address: '',
    is_default: false
  };
  isEditing.value = false;
  editingId.value = null;
  showForm.value = false;
  errorMessage.value = '';
};

// 取得 API URL
const getApiBase = () => process.server ? config.public.apiBase : config.public.apiBaseClient || config.public.apiBase;

// 1. 取得所有地址
const fetchAddresses = async () => {
  const token = userCookie.value?.token;
  if (!token) return navigateTo('/login');

  try {
    isLoading.value = true;
    const response = await $fetch('/address/', {
      baseURL: getApiBase(),
      method: 'GET',
      headers: { 'Authorization': `Bearer ${token}` }
    });
    addresses.value = response || [];
  } catch (err) {
    console.error('取得地址失敗:', err);
    if (err.response?.status === 401 || err.data?.statusCode === 401) {
      userCookie.value = null;
      navigateTo('/login');
    }
  } finally {
    isLoading.value = false;
  }
};

// 打開新增表單
const openAddForm = () => {
  resetForm();
  showForm.value = true;
};

// 打開編輯表單
const openEditForm = (address) => {
  resetForm();
  form.value = { ...address };
  isEditing.value = true;
  editingId.value = address.id;
  showForm.value = true;
};

// 2. 儲存 (新增/修改) 地址
// 電話號碼即時驗證
const validatePhone = () => {
  const phone = form.value.receiver_phone.replace(/[\s-]/g, '');
  if (!phone) {
    phoneError.value = '';
    return;
  }
  if (!/^09\d{0,8}$/.test(phone)) {
    phoneError.value = '手機號碼須為 09 開頭的數字';
  } else if (phone.length < 10) {
    phoneError.value = `還需要輸入 ${10 - phone.length} 碼`;
  } else {
    phoneError.value = '';
  }
};

const handleSave = async () => {
  if (isSaving.value) return;
  
  if (!form.value.receiver_name || !form.value.receiver_phone || !form.value.city || !form.value.district || !form.value.detail_address) {
      errorMessage.value = '除了標籤外，其他欄位皆為必填。';
      return;
  }

  // 電話格式驗證
  const cleanedPhone = form.value.receiver_phone.replace(/[\s-]/g, '');
  if (!/^09\d{8}$/.test(cleanedPhone)) {
    errorMessage.value = '請輸入正確的手機號碼（09 開頭，共 10 碼數字）';
    return;
  }

  isSaving.value = true;
  errorMessage.value = '';
  saveMessage.value = '';

  const token = userCookie.value?.token;
  const endpoint = isEditing.value ? `/address/${editingId.value}/` : '/address/';
  const method = isEditing.value ? 'PUT' : 'POST';

  try {
    await $fetch(endpoint, {
      baseURL: getApiBase(),
      method: method,
      headers: { 'Authorization': `Bearer ${token}` },
      body: form.value
    });

    saveMessage.value = isEditing.value ? '地址已更新成功！' : '新地址已加入地址簿！';
    showFormSuccessMask.value = true;
    await fetchAddresses();
    
    // 2秒後消除遮罩並關閉表單
    setTimeout(() => { 
      showFormSuccessMask.value = false;
      saveMessage.value = ''; 
      resetForm();
    }, 2000);
  } catch (err) {
    errorMessage.value = err.data?.error || '儲存失敗，請檢查欄位格式或稍後再試。';
  } finally {
    isSaving.value = false;
  }
};

// 3. 刪除地址
const deleteAddress = async (id) => {
  if (!confirm('確定要刪除這筆地址嗎？')) return;

  const token = userCookie.value?.token;
  try {
    await $fetch(`/address/${id}/`, {
      baseURL: getApiBase(),
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    });
    // 刪除後重新抓取列表
    await fetchAddresses();
  } catch (err) {
    alert('刪除失敗，請稍後再試。');
  }
};

// 4. 快速設為預設
const setDefault = async (address) => {
  if (address.is_default) return; // 已經是預設了就不用打 API

  const token = userCookie.value?.token;
  try {
    await $fetch(`/address/${address.id}/`, {
      baseURL: getApiBase(),
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${token}` },
      body: { ...address, is_default: true }
    });
    // 卡片內彈出成功遮罩
    settingDefaultId.value = address.id;
    await fetchAddresses();
    setTimeout(() => { 
      settingDefaultId.value = null;
    }, 2000);
  } catch (err) {
    alert('設定失敗，請稍後再試。');
  }
};

onMounted(() => {
  fetchAddresses();
});
</script>

<template>
  <div class="member-page-container">
    <div class="content-wrapper">
      <!-- Left Sidebar -->
      <MemberSidebar />

      <!-- Right Dashboard Content -->
      <main class="dashboard-content">
        <div class="member-banner">
          <div class="banner-info">
            <h1 class="welcome-text">收件地址管理</h1>
            <p class="join-date">管理您的常用收件人與地址，讓結帳更快速。</p>
          </div>
        </div>

        <!-- 成功訊息遮罩移除 (全螢幕版已廢棄) -->

        <!-- 載入中 -->
        <div v-if="isLoading" class="loading-container">
          <div class="loading-spinner"></div>
          <p>載入中...</p>
        </div>

        <template v-else>
          <!-- 地址簿清單 (當沒有在編輯時顯示) -->
          <div v-if="!showForm" class="address-list-section">
            <div class="section-header">
                <h3>我的地址簿 ({{ addresses.length }})</h3>
                <button @click="openAddForm" class="add-new-btn">
                  <svg xmlns="http://www.w3.org/2000/svg" class="plus-icon" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
                  </svg>
                  新增收件地址
                </button>
            </div>

            <!-- 沒有地址的空狀態 -->
            <div v-if="addresses.length === 0" class="empty-state">
                <div class="empty-icon">📍</div>
                <p>您還沒有設定任何常用收件地址</p>
                <span class="empty-hint">預先設定好地址，結帳時就能一鍵帶入，節省您的寶貴時間！</span>
            </div>

            <!-- 地址卡片列表 (加入層級動畫 transition-group) -->
            <transition-group name="list" tag="div" v-else class="address-grid">
               <div v-for="address in addresses" :key="address.id" class="address-card" :class="{ 'is-default-card': address.is_default }">
                 
                 <!-- 卡片內部的成功遮罩 -->
                 <transition name="fade">
                   <div v-if="settingDefaultId === address.id" class="success-overlay card-overlay">
                     <div class="success-content">
                       <div class="success-circle small-circle">
                          <svg xmlns="http://www.w3.org/2000/svg" class="success-icon-large small-icon" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                          </svg>
                       </div>
                       <h4 class="success-title small-title">已設為預設</h4>
                     </div>
                   </div>
                 </transition>

                 <div class="card-top">
                    <div class="address-tags">
                        <span v-if="address.is_default" class="tag default-tag">預設地址</span>
                        <span v-if="address.title" class="tag custom-tag">{{ address.title }}</span>
                    </div>
                    <div class="card-actions">
                        <button @click="openEditForm(address)" class="action-btn edit-btn">編輯</button>
                        <button v-if="!address.is_default" @click="deleteAddress(address.id)" class="action-btn delete-btn">刪除</button>
                    </div>
                 </div>

                 <div class="address-details">
                    <div class="detail-row">
                       <span class="detail-label">收件人</span>
                       <span class="detail-value fw-bold">{{ address.receiver_name }}</span>
                    </div>
                    <div class="detail-row">
                       <span class="detail-label">聯絡電話</span>
                       <span class="detail-value">{{ address.receiver_phone }}</span>
                    </div>
                    <div class="detail-row">
                       <span class="detail-label">收件地址</span>
                       <span class="detail-value">{{ address.city }}{{ address.district }}{{ address.detail_address }}</span>
                    </div>
                 </div>

                 <!-- 底部按鈕 -->
                 <div class="card-bottom" v-if="!address.is_default">
                     <button @click="setDefault(address)" class="set-default-btn">設為預設地址</button>
                 </div>
               </div>
            </transition-group>
          </div>

          <!-- 新增/編輯表單 -->
          <div v-if="showForm" class="info-grid">
             <div class="info-card" style="grid-column: 1 / -1; max-width: 600px; position: relative; overflow: hidden;">
                
                <!-- 成功遮罩 (絕對定位蓋在表單上方) -->
                <transition name="fade">
                  <div v-if="showFormSuccessMask" class="success-overlay">
                    <div class="success-content">
                      <div class="success-circle">
                         <svg xmlns="http://www.w3.org/2000/svg" class="success-icon-large" viewBox="0 0 20 20" fill="currentColor">
                           <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                         </svg>
                      </div>
                      <h4 class="success-title">{{ saveMessage }}</h4>
                    </div>
                  </div>
                </transition>

                <div class="card-header">
                  <h3>{{ isEditing ? '編輯地址' : '新增收件地址' }}</h3>
                </div>
                <div class="card-body">
                  <form @submit.prevent="handleSave" class="profile-form">
                    
                    <!-- 標籤 -->
                    <div class="form-group">
                      <label class="form-label">地址標籤 <span class="optional-text">(選填)</span></label>
                      <input 
                        v-model="form.title" 
                        type="text" 
                        class="form-input" 
                        placeholder="例如：家裡、公司、公婆家" 
                        :disabled="isSaving"
                        maxlength="50"
                      />
                    </div>

                    <!-- 姓名與電話並排 -->
                    <div class="form-row">
                        <div class="form-group half-width">
                          <label class="form-label">收件人姓名 <span class="required-star">*</span></label>
                          <input 
                            v-model="form.receiver_name" 
                            type="text" 
                            class="form-input" 
                            placeholder="請填寫真實姓名" 
                            :disabled="isSaving"
                            required
                          />
                        </div>
                        <div class="form-group half-width">
                          <label class="form-label">聯絡電話 <span class="required-star">*</span></label>
                          <input 
                            v-model="form.receiver_phone" 
                            type="tel" 
                            class="form-input" 
                            :class="{ 'input-error': phoneError }"
                            placeholder="例如：0912345678" 
                            :disabled="isSaving"
                            required
                            maxlength="10"
                            @input="validatePhone"
                          />
                          <span v-if="phoneError" class="field-error">{{ phoneError }}</span>
                        </div>
                    </div>
                    
                    <!-- 縣市與分區並排 (改為下拉選單) -->
                    <div class="form-row">
                        <div class="form-group half-width">
                          <label class="form-label">縣/市 <span class="required-star">*</span></label>
                          <select 
                            v-model="form.city" 
                            class="form-input form-select" 
                            :disabled="isSaving"
                            @change="form.district = taiwanCities[form.city][0]"
                            required
                          >
                            <option v-for="(districts, cityName) in taiwanCities" :key="cityName" :value="cityName">
                              {{ cityName }}
                            </option>
                          </select>
                        </div>
                        <div class="form-group half-width">
                          <label class="form-label">鄉鎮市區 <span class="required-star">*</span></label>
                          <select 
                            v-model="form.district" 
                            class="form-input form-select" 
                            :disabled="isSaving || !form.city"
                            required
                          >
                            <option v-for="district in availableDistricts" :key="district" :value="district">
                              {{ district }}
                            </option>
                          </select>
                        </div>
                    </div>

                    <!-- 詳細地址 (自動帶入縣市與鄉鎮標籤做為視覺提示) -->
                    <div class="form-group">
                      <label class="form-label">詳細地址 <span class="required-star">*</span></label>
                      <div class="address-input-wrapper">
                        <!-- 視覺上的地址前綴標籤 -->
                        <span class="address-prefix" v-if="form.city && form.district">
                          {{ form.city }}{{ form.district }}
                        </span>
                        <input 
                          v-model="form.detail_address" 
                          type="text" 
                          class="form-input joined-input" 
                          placeholder="請接續填寫路名、巷弄、樓層" 
                          :disabled="isSaving"
                          required
                        />
                      </div>
                    </div>

                    <!-- 設為預設 -->
                    <div class="form-group toggle-group" style="padding-top: 10px;">
                      <label class="checkbox-container">
                        <input type="checkbox" v-model="form.is_default" :disabled="isSaving" />
                        <span class="checkmark"></span>
                        <div class="checkbox-text">
                            <strong>設為預設收件地址</strong>
                            <p>未來結帳時，系統將會優先帶入此地址。</p>
                        </div>
                      </label>
                    </div>
  
                    <!-- 錯誤訊息 -->
                    <div v-if="errorMessage" class="error-msg">{{ errorMessage }}</div>
  
                    <!-- 操作按鈕 -->
                    <div class="form-actions form-actions-split">
                      <button type="button" @click="resetForm" class="cancel-btn" :disabled="isSaving">
                        取消
                      </button>
                      <button type="submit" class="submit-btn" :disabled="isSaving">
                        <span v-if="isSaving" class="spinner-small"></span>
                        {{ isSaving ? '儲存中...' : '儲存地址' }}
                      </button>
                    </div>
                    
                  </form>
                </div>
              </div>
          </div>
        </template>
      </main>
    </div>
  </div>
</template>

<style src="@/assets/css/Member_page.css" scoped></style>
<style scoped>
/* 共用 Form 樣式 (沿用自 profile) */
.profile-form { display: flex; flex-direction: column; gap: 20px; }
.form-row { display: flex; gap: 16px; }
.half-width { flex: 1; }
.form-group { display: flex; flex-direction: column; gap: 8px; }
.form-label { font-size: 14px; font-weight: 600; color: #444; }
.required-star { color: #E25E5E; }
.optional-text { font-size: 12px; color: #999; font-weight: normal; }
.form-input { padding: 12px 16px; border: 1px solid #dcdcdc; border-radius: 8px; font-size: 15px; color: #333; transition: all 0.2s; background-color: #fcfcfc; width: 100%; box-sizing: border-box; }
.form-input:focus { border-color: #C1A96C; outline: none; background-color: #ffffff; box-shadow: 0 0 0 3px rgba(193, 169, 108, 0.15); }
.form-input:disabled { background-color: #f0f0f0; cursor: not-allowed; opacity: 0.7; }
.form-select { cursor: pointer; appearance: none; background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e"); background-repeat: no-repeat; background-position: right 1rem center; background-size: 1em; padding-right: 40px; }

/* 詳細地址輸入框外殼 */
.address-input-wrapper { display: flex; align-items: stretch; border: 1px solid #dcdcdc; border-radius: 8px; background-color: #fcfcfc; transition: all 0.2s; overflow: hidden; }
.address-input-wrapper:focus-within { border-color: #C1A96C; box-shadow: 0 0 0 3px rgba(193, 169, 108, 0.15); background-color: #ffffff; }
.address-prefix { background-color: #f0f0f0; color: #555; padding: 12px 16px; border-right: 1px solid #dcdcdc; font-size: 15px; font-weight: 500; display: flex; align-items: center; white-space: nowrap; user-select: none; }
.joined-input { border: none !important; border-radius: 0 !important; background: transparent !important; box-shadow: none !important; flex-grow: 1; min-width: 0; }


/* 勾選框 */
.toggle-group { margin-top: 10px; margin-bottom: 20px; }
.checkbox-container { display: flex; align-items: flex-start; position: relative; padding-left: 28px; cursor: pointer; user-select: none; }
.checkbox-container input { position: absolute; opacity: 0; cursor: pointer; height: 0; width: 0; }
.checkmark { position: absolute; top: 3px; left: 0; height: 20px; width: 20px; background-color: #fff; border: 1px solid #c4c4c4; border-radius: 4px; transition: all 0.2s; }
.checkbox-container:hover input ~ .checkmark { border-color: #C1A96C; }
.checkbox-container input:checked ~ .checkmark { background-color: #C1A96C; border-color: #C1A96C; }
.checkmark:after { content: ""; position: absolute; display: none; }
.checkbox-container input:checked ~ .checkmark:after { display: block; }
.checkbox-container .checkmark:after { left: 6px; top: 2px; width: 5px; height: 10px; border: solid white; border-width: 0 2px 2px 0; transform: rotate(45deg); }
.checkbox-text { display: flex; flex-direction: column; gap: 4px; }
.checkbox-text strong { font-size: 15px; color: #333; }
.checkbox-text p { font-size: 13px; color: #888; margin: 0; line-height: 1.4; }

/* 按鈕 */
.form-actions-split { display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #eee; padding-top: 20px; margin-top: 10px; }
.submit-btn { background-color: #C1A96C; color: white; border: none; padding: 12px 30px; border-radius: 8px; font-size: 15px; font-weight: 600; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; gap: 8px; min-width: 120px; justify-content: center; }
.submit-btn:hover:not(:disabled) { background-color: #b0985c; transform: translateY(-1px); }
.submit-btn:disabled { background-color: #d3d3d3; cursor: not-allowed; transform: none; }
.cancel-btn { background: none; border: 1px solid #ddd; color: #666; padding: 12px 24px; border-radius: 8px; font-size: 15px; font-weight: 500; cursor: pointer; transition: all 0.2s; }
.cancel-btn:hover:not(:disabled) { background-color: #f5f5f5; color: #333; }

/* 列表 Header */
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; border-bottom: 2px solid #f0f0f0; padding-bottom: 16px; }
.section-header h3 { margin: 0; font-size: 18px; color: #333; font-weight: 600; }
.add-new-btn { background-color: #C1A96C; color: white; border: none; padding: 10px 18px; border-radius: 6px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; gap: 6px; box-shadow: 0 2px 8px rgba(193, 169, 108, 0.3); }
.add-new-btn:hover { background-color: #a8925b; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(193, 169, 108, 0.4); }
.plus-icon { width: 16px; height: 16px; }

/* 網格卡片列 */
.address-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
.address-card { background: white; border: 1px solid #eaeaea; border-radius: 12px; padding: 20px; position: relative; transition: all 0.2s; box-shadow: 0 2px 8px rgba(0,0,0,0.02); display: flex; flex-direction: column; overflow: hidden; }
.address-card:hover { border-color: #C1A96C; box-shadow: 0 8px 16px rgba(193, 169, 108, 0.08); transform: translateY(-2px); }
.is-default-card { border: 2px solid #C1A96C; box-shadow: 0 4px 12px rgba(193, 169, 108, 0.1); }

/* 卡片上方標籤與操作區域 */
.card-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; }
.address-tags { display: flex; gap: 8px; flex-wrap: wrap; }
.tag { padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; letter-spacing: 0.5px; }
.default-tag { background-color: #fdf6e3; color: #C1A96C; border: 1px solid #f2e2b3; }
.custom-tag { background-color: #f3f4f6; color: #6b7280; border: 1px solid #e5e7eb; }

/* 編輯與刪除文字鈕 */
.card-actions { display: flex; gap: 12px; }
.action-btn { background: none; border: none; font-size: 13px; font-weight: 500; cursor: pointer; padding: 0; transition: color 0.2s; }
.edit-btn { color: #3b82f6; }
.edit-btn:hover { color: #2563eb; text-decoration: underline; }
.delete-btn { color: #ef4444; }
.delete-btn:hover { color: #dc2626; text-decoration: underline; }

/* 卡片內容細節 */
.address-details { display: flex; flex-direction: column; gap: 10px; flex-grow: 1; }
.detail-row { display: flex; flex-direction: column; gap: 2px; }
.detail-label { font-size: 12px; color: #888; }
.detail-value { font-size: 15px; color: #333; line-height: 1.4; }
.fw-bold { font-weight: 600; font-size: 16px; }

/* 卡片底部 (設為預設鈕) */
.card-bottom { margin-top: 20px; border-top: 1px dashed #eaeaea; padding-top: 16px; }
.set-default-btn { width: 100%; background: none; border: 1px solid #eaeaea; color: #666; padding: 10px; border-radius: 6px; font-size: 13px; font-weight: 500; cursor: pointer; transition: all 0.2s; }
.set-default-btn:hover { background-color: #fcfcfc; border-color: #C1A96C; color: #C1A96C; }

/* 空狀態 */
.empty-state { text-align: center; padding: 60px 20px; background-color: #fcfcfc; border-radius: 12px; border: 1px dashed #ddd; }
.empty-icon { font-size: 40px; margin-bottom: 16px; opacity: 0.6; }
.empty-state p { font-size: 18px; color: #444; font-weight: 600; margin: 0 0 8px 0; }
.empty-hint { font-size: 14px; color: #888; }

/* 全局訊息區 */
.global-success-msg { background-color: #E8F5E9; color: #2F8A3B; padding: 12px 20px; border-radius: 8px; font-weight: 500; margin-bottom: 24px; display: flex; align-items: center; gap: 8px; border: 1px solid #c8e6c9; }
.error-msg { color: #E25E5E; font-size: 14px; background-color: #FEE2E2; padding: 12px 16px; border-radius: 8px; margin-top: 5px; margin-bottom: 15px; border: 1px solid #fecaca; }
.field-error { font-size: 12px; color: #E25E5E; margin-top: 2px; }
.input-error { border-color: #E25E5E !important; }
.input-error:focus { box-shadow: 0 0 0 3px rgba(226, 94, 94, 0.15) !important; }
.spinner-small { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* 成功遮罩 */
.success-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.65); backdrop-filter: blur(3px); z-index: 50; display: flex; align-items: center; justify-content: center; }
.card-overlay { border-radius: 12px; }
.global-fixed-overlay { position: fixed !important; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 9999; }
.success-content { display: flex; flex-direction: column; align-items: center; gap: 16px; animation: scaleUpBounce 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
.success-circle { width: 72px; height: 72px; background-color: #2e8b57; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 16px rgba(46, 139, 87, 0.4); border: 4px solid rgba(255,255,255,0.2); }
.success-icon-large { width: 40px; height: 40px; color: white; stroke-width: 1; }
.success-title { color: white; font-size: 18px; font-weight: 600; letter-spacing: 1px; margin: 0; text-shadow: 0 2px 4px rgba(0,0,0,0.4); }

.small-circle { width: 48px; height: 48px; border-width: 2px; }
.small-icon { width: 28px; height: 28px; }
.small-title { font-size: 14px; margin-top: -6px; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
@keyframes scaleUpBounce {
  0% { transform: scale(0.6); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}

/* 地址列表平滑移動動畫 */
.list-move, .list-enter-active, .list-leave-active { transition: all 0.5s cubic-bezier(0.55, 0, 0.1, 1); }
.list-enter-from, .list-leave-to { opacity: 0; transform: scaleY(0.01) translate(30px, 0); }
.list-leave-active { position: absolute; }

/* RWD 微調 */
@media (max-width: 600px) {
  .form-row { flex-direction: column; gap: 20px; }
  .form-actions-split { flex-direction: column-reverse; gap: 12px; }
  .form-actions-split button { width: 100%; }
}
</style>
