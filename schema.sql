-- ============================================================
-- 우주도서관 Supabase 스키마
-- Supabase 대시보드 > SQL Editor에 이 파일 전체를 붙여넣고 실행하세요.
-- ============================================================

-- [1] 북마크 테이블
CREATE TABLE IF NOT EXISTS bookmarks (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,  -- Supabase 인증 유저와 연결
    title TEXT NOT NULL,
    img_url TEXT,
    description TEXT,
    ai_summary TEXT,                -- AI 해설 저장 (재생성 API 호출 절약)
    collection_name TEXT DEFAULT '기본 컬렉션',
    source_type TEXT,               -- 'apod' 또는 'search'
    source_id TEXT,                 -- 날짜 또는 검색 키워드
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- [2] Row Level Security (RLS) 활성화 - 본인 데이터만 접근 가능
ALTER TABLE bookmarks ENABLE ROW LEVEL SECURITY;

-- [3] 정책: 유저는 자신의 북마크만 조회/삽입/삭제 가능
CREATE POLICY "유저 본인 조회" ON bookmarks
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "유저 본인 삽입" ON bookmarks
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "유저 본인 삭제" ON bookmarks
    FOR DELETE USING (auth.uid() = user_id);

-- [4] 인덱스 (조회 성능 최적화)
CREATE INDEX IF NOT EXISTS idx_bookmarks_user_id ON bookmarks(user_id);
CREATE INDEX IF NOT EXISTS idx_bookmarks_collection ON bookmarks(user_id, collection_name);

-- ============================================================
-- [5] 추천(Referral) 추적 테이블
-- ?ref=CODE URL 파라미터로 유입된 방문자를 기록
-- ============================================================
CREATE TABLE IF NOT EXISTS referrals (
    id         UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    ref_code   TEXT NOT NULL,          -- 추천인 코드 (URL의 ?ref= 값)
    visitor_id TEXT NOT NULL DEFAULT 'guest',  -- 방문자 user_id (비로그인 시 'guest')
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (ref_code, visitor_id)      -- 같은 추천코드+방문자 중복 저장 방지
);

-- RLS: 서비스 관리자(anon key)는 INSERT만, 조회는 비활성화
ALTER TABLE referrals ENABLE ROW LEVEL SECURITY;

CREATE POLICY "referral_insert" ON referrals
    FOR INSERT WITH CHECK (true);

-- [6] 인덱스
CREATE INDEX IF NOT EXISTS idx_referrals_code ON referrals(ref_code);
CREATE INDEX IF NOT EXISTS idx_referrals_created ON referrals(created_at DESC);
