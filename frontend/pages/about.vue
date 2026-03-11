<script setup>
definePageMeta({ layout: 'default' })
</script>

<template>
    <div class="about_page">

        <!-- ============ Hero 橫幅 ============ -->
        <HeroBanner title="關於田原" subtitle="用心栽培每一串葡萄，傳遞土地的溫度" />


        <!-- ============ 品牌故事 ============ -->
        <section class="about_section about_story">
            <div class="about_container about_row">
                <div class="about_text_col">
                    <span class="about_label">Brand Story</span>
                    <h2 class="about_heading">品牌故事</h2>
                    <p class="about_paragraph">
                        田原溫室座落在彰化縣大村鄉，是一片被陽光眷顧的土地。
                        自創立以來，我們始終堅持以最天然的方式栽培葡萄，
                        讓每一顆果實都蘊含著這片土地最純粹的味道。
                    </p>
                    <p class="about_paragraph">
                        從一個小小的夢想出發，我們希望讓更多人品嚐到真正用心種植的葡萄。
                        不使用催熟劑、不搶收，只在最完美的時刻採摘，
                        將大自然的禮物完整送到您的餐桌上。
                    </p>
                </div>
                <div class="about_img_col">
                    <div class="about_img_wrap">
                        <img src="https://images.unsplash.com/photo-1596451190630-186aff535bf2?w=600&h=450&fit=crop" alt="品牌故事" class="about_img">
                    </div>
                </div>
            </div>
        </section>

        <!-- ============ 農場特色 ============ -->
        <section class="about_section about_features">
            <div class="about_container about_row reverse">
                <div class="about_text_col">
                    <span class="about_label">Our Features</span>
                    <h2 class="about_heading">農場特色</h2>
                    <div class="about_feature_list">
                        <div class="about_feature_item">
                            <div class="about_feature_icon"><i class="fas fa-leaf"></i></div>
                            <div>
                                <h4>溫室精緻栽培</h4>
                                <p>採用先進溫室設施，精準控制溫度與溼度，確保每串葡萄都在最佳環境中成長。</p>
                            </div>
                        </div>
                        <div class="about_feature_item">
                            <div class="about_feature_icon"><i class="fas fa-shield-alt"></i></div>
                            <div>
                                <h4>安心無毒承諾</h4>
                                <p>通過農藥殘留檢測，堅持生態友善的種植方式，讓您安心品嚐，放心購買。</p>
                            </div>
                        </div>
                        <div class="about_feature_item">
                            <div class="about_feature_icon"><i class="fas fa-award"></i></div>
                            <div>
                                <h4>產地直送新鮮</h4>
                                <p>採收後 24 小時內出貨，省去中間商環節，以最短的時間將新鮮送到您手中。</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="about_img_col">
                    <div class="about_img_wrap">
                        <img src="https://images.unsplash.com/photo-1573246123716-6b1782bfc499?w=600&h=450&fit=crop" alt="農場特色" class="about_img">
                    </div>
                </div>
            </div>
        </section>

        <!-- ============ 種植流程 ============ -->
        <section class="about_section about_process">
            <div class="about_container">
                <div class="about_section_header">
                    <span class="about_label">Growing Process</span>
                    <h2 class="about_heading">種植流程</h2>
                    <p class="about_subtitle">從一顆嫩芽到甜蜜果實，每一步都傾注心血</p>
                </div>

                <div class="about_timeline">
                    <div class="about_timeline_item">
                        <div class="about_timeline_img_wrap">
                            <img src="https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&h=300&fit=crop" alt="育苗整枝" class="about_timeline_img">
                        </div>
                        <div class="about_timeline_content">
                            <span class="about_timeline_step">01</span>
                            <h4>育苗整枝</h4>
                            <p>精選優質品種嫁接育苗，在適當時機進行整枝修剪，為新一季的成長做準備。</p>
                        </div>
                    </div>

                    <div class="about_timeline_item reverse">
                        <div class="about_timeline_img_wrap">
                            <img src="https://images.unsplash.com/photo-1457530378978-8bac673b8062?w=400&h=300&fit=crop" alt="開花授粉" class="about_timeline_img">
                        </div>
                        <div class="about_timeline_content">
                            <span class="about_timeline_step">02</span>
                            <h4>開花授粉</h4>
                            <p>細心管理開花期的溫濕度，確保授粉成功率，為豐碩的果實打下基礎。</p>
                        </div>
                    </div>

                    <div class="about_timeline_item">
                        <div class="about_timeline_img_wrap">
                            <img src="https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?w=400&h=300&fit=crop" alt="疏果套袋" class="about_timeline_img">
                        </div>
                        <div class="about_timeline_content">
                            <span class="about_timeline_step">03</span>
                            <h4>疏果套袋</h4>
                            <p>人工疏果控制每串數量，再逐一套袋保護，讓營養集中，果粒更加飽滿甜美。</p>
                        </div>
                    </div>

                    <div class="about_timeline_item reverse">
                        <div class="about_timeline_img_wrap">
                            <img src="https://images.unsplash.com/photo-1631729371254-42c2892f0e6e?w=400&h=300&fit=crop" alt="熟成採收" class="about_timeline_img">
                        </div>
                        <div class="about_timeline_content">
                            <span class="about_timeline_step">04</span>
                            <h4>熟成採收</h4>
                            <p>依據糖度檢測與色澤判斷，只在最完美的時刻採收，確保您收到的每一串都是頂級風味。</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- ============ 農場主人 ============ -->
        <section class="about_section about_owner">
            <div class="about_container about_row">
                <div class="about_img_col">
                    <div class="about_img_wrap about_owner_img_wrap">
                        <img src="https://images.unsplash.com/photo-1605000797499-95a51c5269ae?w=500&h=600&fit=crop" alt="農場主人" class="about_img about_owner_img">
                    </div>
                </div>
                <div class="about_text_col about_owner_text">
                    <span class="about_label">Farm Owner</span>
                    <h2 class="about_heading">農場主人</h2>
                    <p class="about_paragraph">
                        「從小看著父親在田裡彎腰耕作，我深知每一份收穫都來之不易。
                        接手田原溫室後，我希望用現代化的技術結合傳統的務農精神，
                        種出讓大家吃了會微笑的葡萄。」
                    </p>
                    <p class="about_paragraph">
                        田原溫室的主人擁有多年葡萄栽培經驗，
                        曾多次前往日本學習先進的溫室種植技術，
                        並將所學融入在地風土，發展出獨特的栽培方法。
                        每一串葡萄，都是對這片土地最深的敬意。
                    </p>
                    <div class="about_owner_signature">
                        <span>— 田原溫室 農場主人</span>
                    </div>
                </div>
            </div>
        </section>

    </div>
</template>

<style src="@/assets/css/AboutPage.css" scoped></style>
